#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def fail(msg):
    print(f"[FAIL] {msg}")
    return False


def ok(msg):
    print(f"[OK] {msg}")
    return True


def warn(msg):
    print(f"[WARN] {msg}")
    return True


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def sha256_path(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_schema(instance, schema):
    try:
        import jsonschema
    except ImportError:
        print("[FAIL] Falta dependencia: pip install jsonschema")
        return False

    try:
        jsonschema.Draft202012Validator(schema).validate(instance)
        return ok("work_order.json cumple el schema local")
    except jsonschema.ValidationError as e:
        route = "/".join(map(str, e.path)) or "<root>"
        return fail(f"Schema local: {e.message} (ruta: {route})")


def validate_semantics(wo):
    valid = True
    verifications = [x["verification"] for x in wo["acceptance"]]

    if not any(v.startswith("validator:") for v in verifications):
        valid &= fail("Falta al menos un validador con umbral")
    else:
        valid &= ok("Hay validador con umbral")

    if not any(v.startswith("test:") for v in verifications):
        valid &= fail("Falta al menos un test nombrado")
    else:
        valid &= ok("Hay test nombrado")

    if not any(v.startswith("ledger:") for v in verifications):
        valid &= fail("Falta al menos una consulta al ledger")
    else:
        valid &= ok("Hay consulta al ledger")

    negative_tokens = ("ningún", "ninguna", " no ", "prohib")
    if not any(
        any(tok in (" " + x["criterion"].lower() + " ") for tok in negative_tokens)
        for x in wo["acceptance"]
    ):
        valid &= fail("No se detectó una restricción negativa")
    else:
        valid &= ok("Hay al menos una restricción negativa")

    if len(wo["no_objectives"]) < 3:
        valid &= fail("Se requieren al menos tres no-objetivos")
    else:
        valid &= ok("Hay al menos tres no-objetivos")

    qb = wo["question_budget"]
    if qb["max_blocking_questions"] > 6 or qb["max_rounds"] > 2:
        valid &= fail("El presupuesto de preguntas excede 6 bloqueantes / 2 rondas")
    else:
        valid &= ok("Presupuesto de preguntas dentro del límite de la guía")

    return bool(valid)


def validate_auction():
    p = ROOT / "auction.json"
    a = load_json(p)
    valid = True

    purchased = sum(i["cost"] for i in a["items"] if i["status"] == "purchased")

    if purchased != a["spent"]:
        valid &= fail("auction.json: spent no coincide con la suma comprada")
    else:
        valid &= ok(f"Subasta consistente: {purchased}/{a['budget_total']} fichas")

    if purchased > a["budget_total"]:
        valid &= fail("La subasta excede 100 fichas")

    not_purchased = [i for i in a["items"] if i["status"] == "not_purchased"]

    if not not_purchased:
        valid &= fail("No hay criterio movido fuera de alcance")
    elif not all(i.get("reopen_condition") for i in not_purchased):
        valid &= fail("Falta condición de reapertura en criterio no comprado")
    else:
        valid &= ok("Criterio no comprado tiene condición de reapertura")

    return bool(valid)


def load_jsonl(path):
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path.name}:{n}: {e}") from e
    return rows


def validate_evals():
    valid = True
    required = {
        "caso_abstencion.jsonl": "abstention",
        "caso_adversario.jsonl": "adversary",
        "caso_agotamiento.jsonl": "budget_exhaustion",
    }

    for fn, typ in required.items():
        p = ROOT / "evals" / fn

        if not p.exists():
            valid &= fail(f"Falta {fn}")
            continue

        try:
            rows = load_jsonl(p)
        except ValueError as e:
            valid &= fail(str(e))
            continue

        if not rows:
            valid &= fail(f"{fn} está vacío")
            continue

        row = rows[0]

        if row.get("case_type") != typ:
            valid &= fail(f"{fn}: case_type incorrecto")
            continue

        if not all(k in row for k in ("input", "initial_state", "expected_verdict")):
            valid &= fail(f"{fn}: faltan input/initial_state/expected_verdict")
            continue

        ev = row["expected_verdict"]

        if typ == "abstention" and not ev.get("missing_evidence"):
            valid &= fail("Abstención: debe nombrar la evidencia que cierra la brecha")
            continue

        if typ == "adversary" and not ev.get("quarantined_fragment"):
            valid &= fail("Adversario: debe contener fragmento puesto en cuarentena")
            continue

        if typ == "budget_exhaustion" and not ev.get("resume_trace"):
            valid &= fail("Agotamiento: debe contener traza de reanudación")
            continue

        valid &= ok(f"{fn} cumple controles mínimos")

    return bool(valid)


def validate_bitacora():
    p = ROOT / "bitacora.md"

    if not p.exists():
        return fail("Falta bitacora.md")

    txt = p.read_text(encoding="utf-8")
    valid = True

    for cid in [f"AC-0{i}" for i in range(1, 6)]:
        if cid not in txt:
            valid &= fail(f"bitacora.md no documenta {cid}")

    if valid:
        valid &= ok("bitacora.md documenta los cinco criterios iniciales")

    return bool(valid)



def validate_external_review_setup():
    required = [
        "prompts/external_review.md",
        "schemas/external_review.json",
        "scripts/run_external_review.py",
        ".github/workflows/external-review.yml",
        ".env.example",
        ".gitignore",
        "docs/external-review.md",
    ]
    missing = [relative for relative in required if not (ROOT / relative).exists()]
    if missing:
        return fail(
            "Configuración de revisión externa incompleta: faltan "
            + ", ".join(missing)
        )

    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    if "google-genai" not in requirements:
        return fail("requirements.txt no incluye google-genai")

    prompt = (ROOT / "prompts" / "external_review.md").read_text(encoding="utf-8")
    if "datos no confiables" not in prompt.lower():
        return fail(
            "El prompt externo no declara los artefactos como datos no confiables"
        )

    return ok("Configuración de revisión externa Gemini completa")

def validate_external_audit():
    latest_path = ROOT / "audits" / "latest.json"
    if not latest_path.exists():
        return warn(
            "Revisión externa preparada pero todavía no ejecutada: no existe audits/latest.json."
        )

    try:
        import jsonschema
    except ImportError:
        return fail("Falta dependencia jsonschema para verificar la auditoría externa")

    latest = load_json(latest_path)
    run_dir = ROOT / latest["run_directory"]
    required = ["request.md", "review.json", "review.md", "manifest.json"]
    missing = [name for name in required if not (run_dir / name).exists()]
    if missing:
        return fail(f"Auditoría externa incompleta: faltan {', '.join(missing)}")

    schema = load_json(ROOT / "schemas" / "external_review.json")
    review = load_json(run_dir / "review.json")
    manifest = load_json(run_dir / "manifest.json")

    try:
        jsonschema.Draft202012Validator(schema).validate(review)
    except jsonschema.ValidationError as e:
        route = "/".join(map(str, e.path)) or "<root>"
        return fail(f"review.json no cumple schema externo: {e.message} ({route})")

    valid = True

    attacks = review["attacks"]
    attacked_ids = {item["criterion_id"] for item in attacks}
    if len(attacks) < 3 or len(attacked_ids) < 3:
        valid &= fail("La auditoría externa no contiene tres ataques sobre criterios distintos")
    else:
        valid &= ok("Auditoría externa contiene al menos tres ataques sobre criterios distintos")

    if not any(item["is_original"] for item in attacks):
        valid &= fail("La auditoría externa no contiene ataque original")
    else:
        valid &= ok("Auditoría externa contiene al menos un ataque original")

    expected = {f"AC-0{i}" for i in range(1, 6)}
    assessed = {item["criterion_id"] for item in review["criteria_assessment"]}
    if assessed != expected:
        valid &= fail("La auditoría externa no evalúa exactamente AC-01...AC-05")
    else:
        valid &= ok("Auditoría externa evalúa exactamente AC-01...AC-05")

    review_hash = sha256_path(run_dir / "review.json")
    request_hash = sha256_path(run_dir / "request.md")

    if review_hash != manifest.get("review_sha256"):
        valid &= fail("Hash de review.json no coincide con manifest.json")
    elif review_hash != latest.get("review_sha256"):
        valid &= fail("Hash de review.json no coincide con audits/latest.json")
    else:
        valid &= ok("Hash de review.json verificado")

    if request_hash != manifest.get("request_sha256"):
        valid &= fail("Hash de request.md no coincide con manifest.json")
    else:
        valid &= ok("Hash de request.md verificado")

    for relative, expected_hash in manifest.get("input_sha256", {}).items():
        path = ROOT / relative
        if not path.exists():
            valid &= fail(f"Entrada auditada ya no existe: {relative}")
            continue
        current_hash = sha256_path(path)
        if current_hash != expected_hash:
            valid &= fail(
                f"Auditoría externa obsoleta: cambió {relative} desde la revisión"
            )

    if valid:
        valid &= ok(
            f"Auditoría externa íntegra: {latest.get('run_id')} / modelo {latest.get('model')}"
        )

    return bool(valid)


def main():
    wo = load_json(ROOT / "work_order.json")
    schema = load_json(ROOT / "schemas" / "work_order.json")

    checks = [
        validate_schema(wo, schema),
        validate_semantics(wo),
        validate_auction(),
        validate_evals(),
        validate_bitacora(),
        validate_external_review_setup(),
        validate_external_audit(),
    ]

    print()

    if all(checks):
        print("VALIDACIÓN LOCAL SUPERADA")
        return 0

    print("VALIDACIÓN LOCAL FALLIDA")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
