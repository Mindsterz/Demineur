import tkinter as tk
from tkinter import messagebox
from random import randrange

def init_grille(M,N,n_mines):

    matrice = [[0 for colonne in range(N)] for ligne in range(M)]                        #On génére la matrice remplit de 0

    for h in range(0,n_mines):                                                           #On génére des indices randoms où mettre les mines
        random_ind_lst = randrange(0, M)
        random_ind_nbr = randrange(0, N)

        while matrice[random_ind_lst][random_ind_nbr] == 'X':                            #On vérifie que l'emplacement de la mine ne soit pas déjà remplit 
            random_ind_lst = randrange(0, M)
            random_ind_nbr = randrange(0, N)

        matrice[random_ind_lst][random_ind_nbr] = 'X'                                    #On place la mine
    
    for ligne in range(M):
        for colonne in range(N):

             if matrice[ligne][colonne] == 'X':                                          #On vérifie si la case est une mine

                 for lgn in range(ligne-1,ligne+2):
                     for col in range(colonne-1,colonne+2):

                         if 0<=lgn<M and 0<=col<N and matrice[lgn][col] != 'X':          #On vérifie que les cases autour ne sont pas des mines et ensuite on incrémente de 1 la valeur des cases autour d'une mine

                             matrice[lgn][col] = matrice[lgn][col]+1


    return matrice

def init_canvas(root, matrice):

    canvas = tk.Canvas(root, background='gray', borderwidth="2")
    canvas.pack()

    idList = []

    for y in range(0,M):
        for x in range(0,N):
            idList.append(canvas.create_rectangle(10+(LARGEUR_CASE*x),10+(HAUTEUR_CASE*y),LARGEUR_CASE+10+(LARGEUR_CASE*x),
            HAUTEUR_CASE+10+(HAUTEUR_CASE*y),fill='grey',outline='light grey'))

    canvas.bind('<Button-1>', lambda event: clic_gauche(event, canvas, matrice))
    canvas.bind('<Button-3>', lambda eventd: clic_droit(eventd, canvas, matrice))

    return canvas,idList

def clic_gauche(event, canvas, matrice):

    x, y = event.x // LARGEUR_CASE, event.y // HAUTEUR_CASE #Calcul les indices de la matrice où l'on a cliqué en utilisant la taille de la case

    if matrice[y][x] == 'X':

        for i in range(len(matrice)):
            for j in range(len(matrice[0])):
                if matrice[i][j] == 'X':
                    canvas.itemconfig(i * len(matrice[0]) + j + 1, fill='red') #Rempli toute les cases contenant des mines de la couleur rouge en cas de clique sur une mine

        messagebox.showinfo("Démineur", "Perdu ! Vous avez cliqué sur une mine.")
        canvas.unbind('<Button-1>')  #Unbind la touche ne permettant plus d'intéragir avec l'interface
    else:
        canvas.itemconfig(y * len(matrice[0]) + x + 1, fill='white')  #Révéle la case et la rempli de blanc quand celle ci n'est pas une mine

def clic_droit(eventd, canvas, matrice):

    x, y = eventd.x // LARGEUR_CASE, eventd.y // HAUTEUR_CASE

    if canvas.itemcget(y * len(matrice[0]) + x + 1, "fill") == "white": #Empêche de mettre un drapeau sur une case déjà révélée
        messagebox.showwarning("Démineur", "La case est déjà révèlée !") #Et affiche un message warning
        return 0

    if canvas.itemcget(y * len(matrice[0]) + x + 1, "fill") == "orange":
        canvas.itemconfig(y * len(matrice[0]) + x + 1, fill="grey")
    else:
        canvas.itemconfig(y * len(matrice[0]) + x + 1, fill="orange")

M = 10 #constante indiquant le nombre de case en y
N = 10 #en x
LARGEUR_CASE = 25 #constante indiquant la "taille" des cases
HAUTEUR_CASE = 25
n_mines = int(input("Nombre de mines ? "))
root = tk.Tk()
root.title("Démineur")
root.geometry('270x290+230+230')
print(init_grille(M,N,n_mines)) #pour voir si la matrice est générée correctement
matrice = init_grille(M, N, n_mines)
init_canvas(root, matrice)
root.mainloop()