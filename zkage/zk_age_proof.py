#!/usr/bin/env python3
"""
zk_age_proof.py - a REAL, runnable, dependency-free non-interactive zero-knowledge proof that
"age >= 18" WITHOUT revealing the birth year. The privacy-preserving alternative to centralized
digital ID / ID-upload age verification: prove the predicate, reveal nothing else, no server.

Construction (all standard, Fiat-Shamir / non-interactive):
  group   : prime-order-q subgroup of Z_p* (RFC 3526 2048-bit safe prime; g=4, h hash-derived)
  commit  : Pedersen  C = g^v * h^r mod p            (hiding + binding)
  issuer  : Schnorr keypair signs the holder's birth-year commitment Cby  (attests identity once)
  proof   : verifier derives Cv = g^(Y-18) * Cby^-1 = commit(age-18, -r); holder proves Cv opens
            to a value in [0, 2^7) via per-bit OR-proofs + a composition (equality) proof.
  reveals : only the boolean "age >= 18". Not the birth year, not the exact age.

Run:  python3 zkage/zk_age_proof.py     (prints a demo + positive/negative tests; exits 0 on success)

NOTE: reference/education code. Real deployments should use audited libraries (e.g. BBS+,
Bulletproofs) and hardware-backed credentials. The point here is to show the PRINCIPLE is buildable
by one person, dependency-free.
"""
import hashlib, secrets, json, sys

# ---- group: RFC 3526 2048-bit MODP safe prime ----
P=int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74"
      "020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374"
      "FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE"
      "386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598D"
      "A48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED5"
      "29077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E7"
      "72C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497"
      "CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
Q=(P-1)//2                      # prime order of the QR subgroup
G=4                             # generator of the order-Q subgroup (QR, != 1)
_hseed=int.from_bytes(hashlib.sha256(b"bubble-map/zkage/h").digest(),"big")
H=pow(_hseed%P or 2,2,P)        # second generator (QR); discrete log base G unknown
NBITS=7                         # age-18 range [0,128): supports ages 18..145

def rnd(): return secrets.randbelow(Q-1)+1
def inv(x): return pow(x,-1,P)
def fs(*xs):                    # Fiat-Shamir challenge in Z_q
    h=hashlib.sha256(); [h.update(int(x).to_bytes((int(x).bit_length()+7)//8 or 1,"big")) for x in xs]
    return int.from_bytes(h.digest(),"big")%Q
def commit(v,r): return (pow(G,v%Q,P)*pow(H,r%Q,P))%P

# ---- Schnorr proof of knowledge of dlog base B: Y = B^x ----
def dlog_prove(B,Y,x):
    k=rnd(); a=pow(B,k,P); e=fs(B,Y,a); z=(k+e*x)%Q; return (a,z)
def dlog_verify(B,Y,pf):
    a,z=pf; e=fs(B,Y,a); return pow(B,z,P)==(a*pow(Y,e,P))%P

# ---- OR proof that C is a Pedersen commitment to a bit (0 or 1), rand s ----
# Y0=C (=h^s if b=0) ; Y1=C*g^-1 (=h^s if b=1) ; prove dlog_h(Y0) OR dlog_h(Y1) known.
def bit_prove(C,b,s):
    Y0=C; Y1=(C*inv(G))%P
    if b==0:
        k0=rnd(); a0=pow(H,k0,P)
        e1=rnd(); z1=rnd(); a1=(pow(H,z1,P)*inv(pow(Y1,e1,P)))%P
        e=fs(C,a0,a1); e0=(e-e1)%Q; z0=(k0+e0*s)%Q
    else:
        k1=rnd(); a1=pow(H,k1,P)
        e0=rnd(); z0=rnd(); a0=(pow(H,z0,P)*inv(pow(Y0,e0,P)))%P
        e=fs(C,a0,a1); e1=(e-e0)%Q; z1=(k1+e1*s)%Q
    return (a0,a1,e0,e1,z0,z1)
def bit_verify(C,pf):
    a0,a1,e0,e1,z0,z1=pf; Y0=C; Y1=(C*inv(G))%P
    if (e0+e1)%Q!=fs(C,a0,a1): return False
    return pow(H,z0,P)==(a0*pow(Y0,e0,P))%P and pow(H,z1,P)==(a1*pow(Y1,e1,P))%P

# ---- range proof: Cv = g^v h^rv  with v in [0,2^NBITS) ----
def range_prove(v,rv):
    assert 0<=v<(1<<NBITS), "value out of range (cannot honestly prove)"
    Cs=[]; bps=[]; s=[]
    for i in range(NBITS):
        bi=(v>>i)&1; si=rnd(); s.append(si)
        Ci=commit(bi,si); Cs.append(Ci); bps.append(bit_prove(Ci,bi,si))
    Cbits=1
    for i,Ci in enumerate(Cs): Cbits=(Cbits*pow(Ci,(1<<i),P))%P
    Sbits=sum((s[i]*(1<<i)) for i in range(NBITS))%Q
    delta=(rv-Sbits)%Q
    Cv=commit(v,rv); D=(Cv*inv(Cbits))%P            # should equal H^delta
    eqpf=dlog_prove(H,D,delta)
    return {"Cs":Cs,"bps":bps,"eq":eqpf}
def range_verify(Cv,pf):
    Cs=pf["Cs"]
    if len(Cs)!=NBITS: return False
    for Ci,bp in zip(Cs,pf["bps"]):
        if not bit_verify(Ci,bp): return False
    Cbits=1
    for i,Ci in enumerate(Cs): Cbits=(Cbits*pow(Ci,(1<<i),P))%P
    D=(Cv*inv(Cbits))%P
    return dlog_verify(H,D,pf["eq"])

# ---- issuer Schnorr signature over the birth-year commitment ----
def issuer_keygen(): sk=rnd(); return sk,pow(G,sk,P)
def issuer_sign(sk,Cby):
    k=rnd(); R=pow(G,k,P); e=fs(pow(G,sk,P),R,Cby); ssig=(k+e*sk)%Q; return (R,ssig)
def issuer_verify(PK,Cby,sig):
    R,ssig=sig; e=fs(PK,R,Cby); return pow(G,ssig,P)==(R*pow(PK,e,P))%P

# ---- holder / verifier roles ----
def holder_get_credential(birth_year,sk_issuer):
    r=rnd(); Cby=commit(birth_year,r); sig=issuer_sign(sk_issuer,Cby)
    return {"Cby":Cby,"r":r,"by":birth_year,"sig":sig}      # r,by stay PRIVATE to holder
def holder_prove_over18(cred,year):
    cutoff=year-18; v=cutoff-cred["by"]
    if not (0<=v<(1<<NBITS)): raise ValueError("cannot honestly prove: under 18 (or >145)")
    rv=(-cred["r"])%Q                                       # Cv = g^cutoff * Cby^-1 = commit(v,-r)
    return {"Cby":cred["Cby"],"sig":cred["sig"],"year":year,"range":range_prove(v,rv)}
def verifier_check(PK_issuer,proof):
    if not issuer_verify(PK_issuer,proof["Cby"],proof["sig"]): return (False,"bad issuer signature")
    cutoff=proof["year"]-18
    Cv=(pow(G,cutoff%Q,P)*inv(proof["Cby"]))%P
    return (range_verify(Cv,proof["range"]), "ok")

def _proof_bytes(p): return json.dumps(p,default=str).encode()

if __name__=="__main__":
    YEAR=2026; ok=True
    sk,PK=issuer_keygen()
    print(f"== Zero-knowledge age>=18 (year {YEAR}) ==  group: RFC3526-2048, NBITS={NBITS}")
    # 1) valid adult
    cred=holder_get_credential(1990,sk)   # 36 yrs old
    pf=holder_prove_over18(cred,YEAR)
    valid,_=verifier_check(PK,pf)
    print(f"[1] adult (born 1990): verifier -> over18={valid}"); ok&=valid
    # privacy: the secret scalars (birth year, exact age, blinding factor) are never transmitted.
    # (They live only inside perfectly-hiding Pedersen commitments; recovering them = breaking dlog.)
    def all_ints(o):
        if isinstance(o,bool): return
        if isinstance(o,int): yield o
        elif isinstance(o,(list,tuple)):
            for x in o: yield from all_ints(x)
        elif isinstance(o,dict):
            for x in o.values(): yield from all_ints(x)
    transmitted=set(all_ints(pf))
    secret_scalars={1990, cred["r"], YEAR-1990}      # birth year, blinding factor, exact age
    leak=secret_scalars & transmitted
    print(f"    privacy: any secret scalar (birth-year/age/blinding) present in transcript? {bool(leak)}")
    print(f"    (birth year is information-theoretically hidden by the Pedersen blinding factor)")
    ok&=(not leak)
    # 2) exactly 18
    pf2=holder_prove_over18(holder_get_credential(YEAR-18,sk),YEAR)
    v2,_=verifier_check(PK,pf2); print(f"[2] exactly 18 (born {YEAR-18}): over18={v2}"); ok&=v2
    # 3) minor cannot produce an honest proof
    try:
        holder_prove_over18(holder_get_credential(YEAR-17,sk),YEAR); print("[3] minor: PROVED (BUG!)"); ok=False
    except ValueError: print("[3] minor (17): prover correctly refuses (no valid range proof)")
    # 4) forged credential (not issuer-signed) is rejected
    forged=holder_get_credential(1990,rnd())   # signed by wrong key
    pf4=holder_prove_over18(forged,YEAR); v4,why=verifier_check(PK,pf4)
    print(f"[4] forged credential: over18={v4} ({why})"); ok&=(not v4)
    # 5) tampered range proof is rejected
    pf5=holder_prove_over18(cred,YEAR); pf5["range"]["Cs"][0]=(pf5["range"]["Cs"][0]*G)%P
    v5,_=verifier_check(PK,pf5); print(f"[5] tampered proof: over18={v5}"); ok&=(not v5)
    print("\nALL CHECKS PASSED" if ok else "\n!! CHECK FAILED"); sys.exit(0 if ok else 1)
