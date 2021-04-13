from cx_Freeze import setup, Executable

setup(
    name= "codec",
    version= "0.1",
    description= "Projet de codage et décodage d'un fichier",
    executables= [Executable("codec.py")]
)