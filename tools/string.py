def escape(s: str) -> str:
    ns = ""
    for c in s:
        if c in "\\`*_{}[]()#+-!":
            ns += "\\"
        ns += c
    return ns.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
