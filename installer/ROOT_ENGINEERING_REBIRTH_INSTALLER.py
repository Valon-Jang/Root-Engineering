#!/usr/bin/env python3
"""Root Engineering 1.0 — Rebirth RC.1.

Single-file installer and deterministic local-state helper for an ordinary
ChatGPT conversation. This program does not compact ChatGPT context; it
protects and records state around a host-owned compaction event.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys, tempfile, uuid, zipfile
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0-rc.1"
DEFAULT_ROOT = Path("/mnt/data/root-engineering")
REQUIRED = (
    "BOOT.md","PROTOCOL.md","ROOT.md","MANIFEST.json",
    "knowledge/FOUNDATION.md","knowledge/CURRENT.md","knowledge/LEARNED.md",
    "knowledge/OPERATIONAL.md","knowledge/HISTORY.md",
    "runtime/CHECKPOINT.md","runtime/STATE.json","runtime/CAPABILITIES.json",
    "sources/INDEX.md","tools/rebirth_runtime.py","tools/noop_boundary.py",
)
CANON = (
    "ROOT.md","knowledge/FOUNDATION.md","knowledge/CURRENT.md",
    "knowledge/LEARNED.md","knowledge/OPERATIONAL.md",
    "knowledge/HISTORY.md","sources/INDEX.md",
)

PROTOCOL = """# ROOT ENGINEERING 1.0 — REBIRTH PROTOCOL

Package Version: 1.0.0-rc.1

> Model is replaceable. Context is replaceable. Root persists. The thread continues.

## Memory Layers
- Chat Transcript: human-visible history.
- Active Model Context: compactable working memory.
- Local ROOT: durable canonical project state.
- CHECKPOINT: transient state required to resume current work.

Compaction is not transcript deletion. Do not claim deletion of provider-side raw records.

## Boot
For project-dependent work read BOOT, ROOT, then CHECKPOINT when resuming.
Read only the canonical owner required by the task. Read this Protocol before
protected writes, migration, repair, export, or compaction.

## Save Placement
- FOUNDATION: stable purpose, principles, boundaries, Human Intent.
- CURRENT: current facts, decisions, constraints, status, important unresolved.
- LEARNED: verified reusable methods and generalized lessons.
- OPERATIONAL: exact operation keys, known failures, do-not-repeat rules,
  verified hot paths, required evidence.
- HISTORY: superseded states with transition, rollback, or prevention value.
- sources/INDEX: evidence pointers and provenance.
- ROOT: identity, digest, routing, topology only.
- CHECKPOINT: current goal, completed work, unresolved work, exact next action.

Do not dump the transcript into ROOT or CHECKPOINT.

## Write Gate
Read the latest exact target, route to the smallest owner, apply the minimum
semantic change, write atomically, read back, and verify. Unverified inference
cannot become canonical fact. Save failure means no compaction.

## Rebirth Transaction
When the user says 압축해 / 컴팩션 / 리버스 / rebirth:

1. Say: 현재 작업을 저장 중입니다…
2. Promote new durable state to the correct canonical owners.
3. Write CHECKPOINT with the exact next action and resume instruction.
4. Run `verify`, then `prepare-compact`.
5. Only after success say: 저장 완료. 대화를 압축 중입니다…
6. Prefer an explicit native compact action actually exposed by the host.
7. Otherwise use exactly one zero-output boundary only when previously verified
   under matching conditions and compaction can be observed.
8. Never invent a private RPC. Never default to thousands of pressure lines.
9. On observed success run `complete-compact --observed`; otherwise abort.
10. Read BOOT, ROOT, CHECKPOINT and only required owners.
11. Say: 압축 완료. 이어서 진행할게.
12. Continue the exact next action in the same chat.

## Capability Evidence
CAPABILITIES.json stores evidence, not assumptions:
native compact = UNKNOWN/AVAILABLE/UNAVAILABLE;
zero-output boundary = UNKNOWN/VERIFIED/REJECTED;
success signal = UNKNOWN/HOST_EVENT/CONTEXT_REPLACEMENT_OBSERVED/MANUAL_CONFIRMATION.
Reverify after host/runtime changes.

## Storage Boundary
The local Root is canonical for the current persistent thread. `/mnt/data`
lifetime is host-controlled and is not universally guaranteed. Export a ZIP at
important milestones. Google Drive/GitHub may be optional backup adapters, not
routine dependencies.

## Migration
Migrate 0.x only on explicit request. Verify the old Root and boundary, map
semantics to local owners, preserve source IDs/URLs, put in-flight work in
CHECKPOINT, do not modify the old Root, and verify the local digest.

## Recovery
Never advance context epoch without evidence. If a pending transaction exists,
inspect CHECKPOINT and state. Abort if compaction was not observed. If the local
Root is missing, restore from a verified snapshot rather than fabricating it.
"""

def md(title: str, role: str, sections: tuple[str, ...]) -> str:
    out = f"# {title}\n\n- Package Version: {VERSION}\n- Project ID: {{PROJECT_ID}}\n- Root ID: {{ROOT_ID}}\n- Role: {role}\n\n"
    for section in sections:
        out += f"## {section}\n\nNone recorded.\n\n"
    return out

TEMPLATES = {
"BOOT.md": """# ROOT ENGINEERING 1.0 — REBIRTH BOOT
- Package Version: 1.0.0-rc.1
- Root Home: {ROOT_HOME}
- Project ID: {PROJECT_ID}
- Root ID: {ROOT_ID}

Project work: ROOT → CHECKPOINT when resuming → only required owner.
Protected write/repair/migration/compaction: read PROTOCOL first.
압축해: Persist → Checkpoint → Verify → Compact → Rehydrate.
Save failure means no compaction.
""",
"ROOT.md": """# PROJECT ROOT
## Root Identity
- Project Name: {PROJECT_NAME}
- Project ID: {PROJECT_ID}
- Root ID: {ROOT_ID}
- Root Home: {ROOT_HOME}
- Package Version: 1.0.0-rc.1
- Storage Adapter: chat-local-filesystem

## Current Digest
- Status: Rebirth local runtime installed.
- Active decision: one primary chat, local Root, explicit verified compaction.
- Important unresolved: initialize project-specific purpose and current work.

## Root Map
- Foundation: `knowledge/FOUNDATION.md`
- Current Knowledge: `knowledge/CURRENT.md`
- Learned Knowledge: `knowledge/LEARNED.md`
- Operational Memory: `knowledge/OPERATIONAL.md`
- History: `knowledge/HISTORY.md`
- Sources: `sources/INDEX.md`
- Runtime Checkpoint: `runtime/CHECKPOINT.md`
""",
"knowledge/FOUNDATION.md": md("Foundation","Stable purpose, principles, boundaries, and Human Intent.",("Project Purpose","Core Principles","Long-term Boundaries","Human Intent")),
"knowledge/CURRENT.md": md("Current Knowledge","Current facts, decisions, constraints, status, and unresolved items.",("Current Status","Active Decisions","Constraints","Important Unresolved")),
"knowledge/LEARNED.md": md("Learned Knowledge","Verified reusable methods and generalized lessons.",("Verified Methods","Reusable Lessons","Applicability Boundaries","Verification Evidence")),
"knowledge/OPERATIONAL.md": md("Operational Memory","Exact operation keys, failures, do-not-repeat rules, hot paths, and evidence gates.",("Fast-Path Index","Operational Records","Known Failure Constraints","Promotion Evidence")),
"knowledge/HISTORY.md": md("History","Superseded states with transition, rollback, or prevention value.",("Superseded Decisions","Transition Rationale","Rollback Notes","Archived Failure Evidence")),
"runtime/CHECKPOINT.md": """# ACTIVE CHECKPOINT
- Package Version: 1.0.0-rc.1
## Checkpoint Metadata
- Project ID: {PROJECT_ID}
- Root ID: {ROOT_ID}
- Transaction ID: NONE
- Checkpoint Time: {TIMESTAMP}
- Context Epoch Before Compact: 0
- Status: IDLE
## Current Goal
Complete Rebirth installation and begin project work.
## Active Work
Installation verification.
## Completed Since Last Checkpoint
Local Root initialized.
## Durable State Promoted
Initial runtime structure.
## Important Unresolved
Project-specific purpose and first active work item.
## Exact Next Action
Continue with the user's next project request.
## Resume Instruction
Read BOOT, ROOT, and this Checkpoint. Load only owners required by Exact Next Action.
""",
"sources/INDEX.md": """# SOURCE INDEX
- Package Version: 1.0.0-rc.1
- Project ID: {PROJECT_ID}
- Root ID: {ROOT_ID}
| Source ID | Title | Location / URL | Authority / Scope | State | Notes |
|---|---|---|---|---|---|
""",
}

def checkpoint_text(project_id: str, root_id: str, state: dict, *, goal: str, active_work: str, completed: str, promoted: str, unresolved: str, next_action: str, resume: str, transaction_id: str = "NONE", status: str = "IDLE") -> str:
    return f"""# ACTIVE CHECKPOINT
- Package Version: {VERSION}
## Checkpoint Metadata
- Project ID: {project_id}
- Root ID: {root_id}
- Transaction ID: {transaction_id}
- Checkpoint Time: {now()}
- Context Epoch Before Compact: {int(state.get('context_epoch', 0))}
- Status: {status}
## Current Goal
{goal.strip()}
## Active Work
{active_work.strip()}
## Completed Since Last Checkpoint
{completed.strip()}
## Durable State Promoted
{promoted.strip()}
## Important Unresolved
{unresolved.strip()}
## Exact Next Action
{next_action.strip()}
## Resume Instruction
{resume.strip()}
"""

class RebirthError(RuntimeError): pass

def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp = Path(name)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as f:
            f.write(text); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if tmp.exists(): tmp.unlink()

def atomic_json(path: Path, obj: dict) -> None:
    atomic_text(path,json.dumps(obj,ensure_ascii=False,indent=2)+"\n")

def read_json(path: Path) -> dict:
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e: raise RebirthError(f"missing: {path}") from e
    except json.JSONDecodeError as e: raise RebirthError(f"invalid JSON {path}: {e}") from e
    if not isinstance(value,dict): raise RebirthError(f"JSON root is not object: {path}")
    return value

def hash_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def digest(root: Path) -> tuple[str,dict]:
    items={}; h=hashlib.sha256()
    for rel in CANON:
        p=root/rel
        if not p.is_file(): raise RebirthError(f"missing canonical file: {rel}")
        d=hash_file(p); items[rel]=d
        h.update(rel.encode()); h.update(b"\0"); h.update(d.encode()); h.update(b"\n")
    return h.hexdigest(),items

def preflight(workspace: Path) -> dict:
    workspace=workspace.resolve(); workspace.mkdir(parents=True,exist_ok=True)
    probe=workspace/f"RE_REBIRTH_PREFLIGHT_{uuid.uuid4().hex[:8].upper()}"
    a=f"A-{uuid.uuid4().hex}"; b=f"B-{uuid.uuid4().hex}"; p=probe/"token.txt"
    try:
        probe.mkdir(); atomic_text(p,a)
        if p.read_text(encoding="utf-8")!=a: raise RebirthError("initial readback mismatch")
        atomic_text(p,b)
        if p.read_text(encoding="utf-8")!=b: raise RebirthError("atomic readback mismatch")
    finally:
        if probe.exists(): shutil.rmtree(probe)
    return {"ok":True,"workspace":str(workspace),"writable":True,"readback":True,"atomic_replace":True,"verified_at":now()}

def install(root: Path, project_name: str, project_id: str|None, root_id: str|None, env: str) -> dict:
    root=root.resolve()
    if root.exists() and any(root.iterdir()):
        if (root/"MANIFEST.json").is_file() and read_json(root/"MANIFEST.json").get("package_version")==VERSION:
            return verify(root)
        raise RebirthError("target exists and is not an exact current Rebirth installation")
    pf=preflight(root.parent); ts=now()
    project_id=project_id or f"REP-{uuid.uuid4().hex[:12].upper()}"
    root_id=root_id or f"RR-{uuid.uuid4().hex[:16].upper()}"
    vals={"ROOT_HOME":str(root),"PROJECT_NAME":project_name,"PROJECT_ID":project_id,"ROOT_ID":root_id,"TIMESTAMP":ts}
    try:
        for rel,text in TEMPLATES.items(): atomic_text(root/rel,text.format(**vals))
        atomic_text(root/"PROTOCOL.md",PROTOCOL)
        atomic_text(root/"tools/rebirth_runtime.py",Path(__file__).read_text(encoding="utf-8"))
        atomic_text(root/"tools/noop_boundary.py","pass\n")
        manifest={"package_id":"root-engineering-rebirth","package_version":VERSION,"schema_version":"1.0.0","codename":"Rebirth","status":"INSTALLING","project_name":project_name,"project_id":project_id,"root_id":root_id,"root_home":str(root),"storage_adapter":"chat-local-filesystem","created_at":ts,"updated_at":ts,"required_paths":list(REQUIRED)}
        state={"package_version":VERSION,"project_id":project_id,"root_id":root_id,"status":"INSTALLING","context_epoch":0,"compaction_count":0,"root_revision":0,"canonical_digest":None,"last_checkpoint_at":None,"last_compaction":None,"pending_compaction":None,"last_error":None,"updated_at":ts}
        caps={"package_version":VERSION,"project_id":project_id,"root_id":root_id,"environment_fingerprint":env,"local_workspace":{"path":str(root),"writable":"VERIFIED","atomic_replace":"VERIFIED","readback":"VERIFIED"},"compaction":{"native_compact_action":"UNKNOWN","zero_output_boundary":"UNKNOWN","success_signal":"UNKNOWN","transcript_retention_observed":"UNKNOWN","scope_note":"Reverify after host/runtime change."},"backup":{"external_adapter":"OPTIONAL","last_export_at":None,"last_export_path":None},"updated_at":ts}
        atomic_json(root/"MANIFEST.json",manifest); atomic_json(root/"runtime/STATE.json",state); atomic_json(root/"runtime/CAPABILITIES.json",caps)
        check=verify(root); d=check["canonical_digest"]
        manifest["status"]="ACTIVE"; manifest["updated_at"]=now()
        state.update({"status":"ACTIVE","canonical_digest":d,"root_revision":1,"updated_at":now()})
        atomic_json(root/"MANIFEST.json",manifest); atomic_json(root/"runtime/STATE.json",state)
        return {"installed":True,"preflight":pf,**verify(root)}
    except Exception:
        if (root/"runtime/STATE.json").is_file():
            try:
                s=read_json(root/"runtime/STATE.json"); s["status"]="FAILED"; s["last_error"]={"at":now(),"reason":"installation failed"}; atomic_json(root/"runtime/STATE.json",s)
            except Exception: pass
        raise

def verify(root: Path) -> dict:
    root=root.resolve(); missing=[x for x in REQUIRED if not (root/x).is_file()]
    if missing: raise RebirthError("missing required paths: "+", ".join(missing))
    m=read_json(root/"MANIFEST.json"); s=read_json(root/"runtime/STATE.json"); c=read_json(root/"runtime/CAPABILITIES.json")
    for k in ("project_id","root_id"):
        if not m.get(k) or m.get(k)!=s.get(k) or m.get(k)!=c.get(k): raise RebirthError(f"identity mismatch: {k}")
    if m.get("package_version")!=VERSION or s.get("package_version")!=VERSION: raise RebirthError("package version mismatch")
    if Path(str(m.get("root_home",""))).resolve()!=root: raise RebirthError("root_home mismatch")
    cp=(root/"runtime/CHECKPOINT.md").read_text(encoding="utf-8")
    if "## Exact Next Action" not in cp or "## Resume Instruction" not in cp: raise RebirthError("checkpoint resume sections missing")
    if f"- Project ID: {m['project_id']}" not in cp or f"- Root ID: {m['root_id']}" not in cp:
        raise RebirthError("checkpoint identity mismatch")
    d,hashes=digest(root)
    return {"ok":True,"root_home":str(root),"project_id":m["project_id"],"root_id":m["root_id"],"manifest_status":m.get("status"),"runtime_status":s.get("status"),"context_epoch":int(s.get("context_epoch",0)),"compaction_count":int(s.get("compaction_count",0)),"root_revision":int(s.get("root_revision",0)),"canonical_digest":d,"canonical_hashes":hashes,"pending_compaction":s.get("pending_compaction")}

def write_checkpoint(root: Path, *, goal: str, active_work: str, completed: str, promoted: str, unresolved: str, next_action: str, resume: str) -> dict:
    check=verify(root); sp=root/"runtime/STATE.json"; s=read_json(sp)
    if s.get("pending_compaction"): raise RebirthError("cannot replace checkpoint while compaction is pending")
    text=checkpoint_text(check["project_id"],check["root_id"],s,goal=goal,active_work=active_work,completed=completed,promoted=promoted,unresolved=unresolved,next_action=next_action,resume=resume)
    cp=root/"runtime/CHECKPOINT.md"; atomic_text(cp,text)
    if hash_file(cp)!=hashlib.sha256(text.encode("utf-8")).hexdigest(): raise RebirthError("checkpoint readback hash mismatch")
    s.update({"last_checkpoint_at":now(),"last_error":None,"updated_at":now()}); atomic_json(sp,s)
    return {"ok":True,"checkpoint":str(cp),"checkpoint_sha256":hash_file(cp),"context_epoch":int(s.get("context_epoch",0))}

def prepare(root: Path, reason: str) -> dict:
    check=verify(root)
    if check["manifest_status"]!="ACTIVE": raise RebirthError("manifest is not ACTIVE")
    sp=root/"runtime/STATE.json"; s=read_json(sp)
    if s.get("pending_compaction"): raise RebirthError("compaction already pending")
    cp=root/"runtime/CHECKPOINT.md"; text=cp.read_text(encoding="utf-8")
    if "## Exact Next Action" not in text or "## Resume Instruction" not in text: raise RebirthError("checkpoint incomplete")
    d=check["canonical_digest"]; rev=int(s.get("root_revision",0))+(d!=s.get("canonical_digest"))
    tx={"transaction_id":f"RC-{uuid.uuid4().hex[:12].upper()}","status":"READY_TO_COMPACT","reason":reason,"prepared_at":now(),"context_epoch_before":int(s.get("context_epoch",0)),"root_revision":rev,"canonical_digest":d,"checkpoint_sha256":hash_file(cp)}
    s.update({"status":"READY_TO_COMPACT","root_revision":rev,"canonical_digest":d,"last_checkpoint_at":tx["prepared_at"],"pending_compaction":tx,"last_error":None,"updated_at":tx["prepared_at"]})
    atomic_json(sp,s)
    if read_json(sp).get("pending_compaction",{}).get("transaction_id")!=tx["transaction_id"]: raise RebirthError("transaction readback failed")
    return tx

def complete(root: Path, observed: bool, method: str, signal: str) -> dict:
    if not observed: raise RebirthError("--observed is required")
    check=verify(root); sp=root/"runtime/STATE.json"; s=read_json(sp); tx=s.get("pending_compaction")
    if not isinstance(tx,dict) or tx.get("status")!="READY_TO_COMPACT": raise RebirthError("no ready transaction")
    if check["canonical_digest"]!=tx.get("canonical_digest"):
        raise RebirthError("canonical state changed after prepare; abort and prepare again")
    cp=root/"runtime/CHECKPOINT.md"
    if hash_file(cp)!=tx.get("checkpoint_sha256"):
        raise RebirthError("checkpoint changed after prepare; abort and prepare again")
    done={**tx,"status":"COMPLETED","completed_at":now(),"context_epoch_after":int(s.get("context_epoch",0))+1,"method":method,"success_signal":signal}
    s.update({"status":"ACTIVE","context_epoch":done["context_epoch_after"],"compaction_count":int(s.get("compaction_count",0))+1,"last_compaction":done,"pending_compaction":None,"last_error":None,"updated_at":done["completed_at"]}); atomic_json(sp,s)
    caps_path=root/"runtime/CAPABILITIES.json"; caps=read_json(caps_path); comp=caps.setdefault("compaction",{})
    if method=="native": comp["native_compact_action"]="AVAILABLE"
    if method=="zero-output-boundary": comp["zero_output_boundary"]="VERIFIED"
    comp["success_signal"]=signal; comp["last_verified_at"]=done["completed_at"]; caps["updated_at"]=done["completed_at"]; atomic_json(caps_path,caps)
    return done

def abort(root: Path, reason: str) -> dict:
    sp=root/"runtime/STATE.json"; s=read_json(sp); tx=s.get("pending_compaction")
    if not isinstance(tx,dict): raise RebirthError("no pending transaction")
    e={"transaction_id":tx.get("transaction_id"),"status":"ABORTED","reason":reason,"aborted_at":now()}
    s.update({"status":"ACTIVE","pending_compaction":None,"last_error":e,"updated_at":e["aborted_at"]}); atomic_json(sp,s); return e

def export(root: Path, output: Path|None) -> Path:
    verify(root); stamp=datetime.now().strftime("%Y%m%d-%H%M%S"); output=(output or root.parent/f"root-engineering-rebirth-{stamp}.zip").resolve()
    with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file() and "scratch" not in p.relative_to(root).parts and "__pycache__" not in p.parts: z.write(p,str(Path("root-engineering")/p.relative_to(root)))
    c=read_json(root/"runtime/CAPABILITIES.json"); c["backup"].update({"last_export_at":now(),"last_export_path":str(output)}); c["updated_at"]=now(); atomic_json(root/"runtime/CAPABILITIES.json",c); return output

def selftest() -> dict:
    tmp=Path(tempfile.mkdtemp(prefix="rebirth-selftest-"))
    try:
        root=tmp/"root"; install(root,"Self Test","REP-TEST","RR-TEST","self-test")
        a=verify(root)
        ck=write_checkpoint(root,goal="Test Rebirth",active_work="Run transaction",completed="Install",promoted="Initial state",unresolved="None",next_action="Prepare compaction",resume="Read BOOT, ROOT, and CHECKPOINT; continue next action.")
        tx=prepare(root,"self-test"); b=abort(root,"expected")
        tx2=prepare(root,"self-test"); c=complete(root,True,"manual-confirmation","MANUAL_CONFIRMATION")
        out=export(root,tmp/"snapshot.zip"); final=verify(root)
        assert a["context_epoch"]==0 and ck["ok"] and b["status"]=="ABORTED" and c["context_epoch_after"]==1 and out.is_file() and final["context_epoch"]==1
        # A sealed transaction must fail closed if its checkpoint changes.
        tx3=prepare(root,"tamper-test"); atomic_text(root/"runtime/CHECKPOINT.md",(root/"runtime/CHECKPOINT.md").read_text()+"\nchanged\n")
        blocked=False
        try: complete(root,True,"diagnostic","CONTEXT_REPLACEMENT_OBSERVED")
        except RebirthError: blocked=True
        assert blocked; abort(root,"tamper correctly blocked")
        return {"ok":True,"tests":8,"version":VERSION}
    finally: shutil.rmtree(tmp)

def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=DEFAULT_ROOT); sub=p.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("install"); i.add_argument("--project-name",default=f"Project_{datetime.now():%Y%m%d}_{uuid.uuid4().hex[:6].upper()}"); i.add_argument("--project-id"); i.add_argument("--root-id"); i.add_argument("--environment-fingerprint",default="ChatGPT chat-local Python workspace")
    sub.add_parser("preflight").add_argument("--workspace",type=Path,default=Path("/mnt/data"))
    sub.add_parser("verify"); sub.add_parser("status")
    x=sub.add_parser("checkpoint")
    x.add_argument("--goal",required=True); x.add_argument("--active-work",required=True); x.add_argument("--completed",required=True); x.add_argument("--promoted",required=True); x.add_argument("--unresolved",required=True); x.add_argument("--next-action",required=True); x.add_argument("--resume",required=True)
    x=sub.add_parser("prepare-compact"); x.add_argument("--reason",default="user-requested")
    x=sub.add_parser("complete-compact"); x.add_argument("--observed",action="store_true"); x.add_argument("--method",choices=["native","zero-output-boundary","diagnostic","manual-confirmation"],required=True); x.add_argument("--signal",choices=["HOST_EVENT","CONTEXT_REPLACEMENT_OBSERVED","MANUAL_CONFIRMATION"],required=True)
    x=sub.add_parser("abort-compact"); x.add_argument("--reason",required=True)
    x=sub.add_parser("export"); x.add_argument("--output",type=Path)
    sub.add_parser("self-test"); return p

def main() -> int:
    a=parser().parse_args(); root=a.root.resolve()
    try:
        if a.cmd=="install": result=install(root,a.project_name,a.project_id,a.root_id,a.environment_fingerprint)
        elif a.cmd=="preflight": result=preflight(a.workspace)
        elif a.cmd=="verify": result=verify(root)
        elif a.cmd=="status": result={"verify":verify(root),"state":read_json(root/"runtime/STATE.json")}
        elif a.cmd=="checkpoint": result=write_checkpoint(root,goal=a.goal,active_work=a.active_work,completed=a.completed,promoted=a.promoted,unresolved=a.unresolved,next_action=a.next_action,resume=a.resume)
        elif a.cmd=="prepare-compact": result=prepare(root,a.reason)
        elif a.cmd=="complete-compact": result=complete(root,a.observed,a.method,a.signal)
        elif a.cmd=="abort-compact": result=abort(root,a.reason)
        elif a.cmd=="export": result={"output":str(export(root,a.output))}
        elif a.cmd=="self-test": result=selftest()
        else: raise RebirthError("unsupported command")
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except RebirthError as e:
        print(f"REBIRTH_ERROR: {e}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
