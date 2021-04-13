# -*-coding:Latin-1 -*

import numpy as np
from tkinter import *
from tkinter.filedialog import *
import re
import time

extension = ""
key = []
file_content = []
file_selected = FALSE
key_selected = FALSE
error = ""

window = Tk()
window.title("Codec")
window.minsize(200, 200)
window.iconbitmap("logo.ico")
window.config(background='#41B77F')


def select_file_key():
    global key
    global key_selected

    filename = askopenfilename(title="Ouvrir votre clé de chiffrement",
                               filetypes=[('txt files', '.txt')])
    file_key = open(filename, "r")
    content = file_key.read()

    regex = r"^G4C=\[(0|1){8}(\s(0|1){8}){3}\]\s*$"
    if re.match(regex, content):
        print("Clé OK")
    else:
        print("Erreur clé non valide")
        return -1
    left = content.index('[')
    right = content.index(']')
    key = content[left + 1:right]
    key = key.replace(" ", "")
    file_key.close()
    key_selected = TRUE


def select_file():
    global extension
    global file_content
    global file_selected

    filename = askopenfilename(title="Ouvrir votre fichier à déchiffrer ou à chiffrer",
                               filetypes=[('all files', '.*')])
    delimiter = filename.index('.')
    if filename[len(filename) - 1] == "c":
        extension = filename[delimiter:-1]
    else:
        extension = filename[delimiter:]

    file = open(filename, "rb")
    file_content = list(file.read())
    file.close()
    file_selected = TRUE


def file_decryption():
    global key
    global file_content
    global file_selected
    global key_selected
    global window

    if file_selected == FALSE or key_selected == FALSE:
        return -1

    identity_matrix = np.eye(4)
    key_matrix = np.zeros((4, 8), dtype=np.byte)
    counter = 0
    final_key = []

    # --------------------------------------------------------
    # Boucle pour ranger la matrice G4C dans une matrice numpy
    for i in range(4):
        for j in range(8):
            key_matrix[i, j] = key[counter]
            counter = counter + 1

    for k in range(4):
        for l in range(8):
            if np.array_equal(key_matrix[:, l], identity_matrix[:, k]):
                final_key.append(l)

    bytes_group = [bin(code)[2:].zfill(8) for code in file_content]

    binary_message = []

    for i in range(len(bytes_group)):
        for j in range(4):
            binary_message.append(bytes_group[i][final_key[j]])

    binary_message = ''.join(binary_message)
    message = bytes(int(binary_message[i: i + 8], 2) for i in range(0, len(binary_message), 8))
    file = open("REPONSE" + extension, "wb")
    file.write(message)
    file.close()
    window.destroy()


def file_encryption():
    global key
    global file_content
    global extension
    global file_selected
    global key_selected
    global window

    if file_selected == FALSE or key_selected == FALSE:
        return -1

    key_matrix = np.zeros((4, 8), dtype=np.byte)
    result = []
    counter = 0

    # --------------------------------------------------------
    # Boucle pour ranger la matrice G4C dans une matrice numpy
    for i in range(4):
        for j in range(8):
            key_matrix[i, j] = key[counter]
            counter = counter + 1

    bytes_group = [bin(code)[2:].zfill(8) for code in file_content]

    for i in range(len(bytes_group)):
        for j in range(0, 8, 4):
            inter = np.asarray(list(bytes_group[i][j:j + 4]), dtype=np.byte) @ key_matrix

            for m in range(8):
                if inter[m] > 1:
                    if inter[m] % 2 == 0:
                        inter[m] = 0
                    else:
                        inter[m] = 1

                result.append(str(inter[m]))

    result = ''.join(result)
    message = bytes(int(result[i: i + 8], 2) for i in range(0, len(result), 8))

    file = open("REPONSE_CODE" + extension + "c", "wb")
    file.write(message)
    file.close()
    window.destroy()


bouton = Button(window, text="Ouvrir la clé de cryptage", command=select_file_key)
bouton.pack()

bouton1 = Button(window, text="Ouvrir le fichier à coder ou décoder", command=select_file)
bouton1.pack()

bouton2 = Button(window, text="Décoder", command=file_decryption)
bouton2.pack()

bouton3 = Button(window, text="Coder", command=file_encryption)
bouton3.pack()

window.mainloop()

# print(time.process_time())
