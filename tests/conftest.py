import warnings

# Silenciar DeprecationWarning específico de python-jose que usa datetime.utcnow()
warnings.filterwarnings(
    "ignore",
    message=r".*datetime.datetime.utcnow.*",
    category=DeprecationWarning,
)

# También filtrar las advertencias deprecación originadas en el módulo jose.jwt
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"jose\.jwt",
)
