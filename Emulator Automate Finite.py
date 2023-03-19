import sys
import tkinter as tk

def progr(date_intrare , fisier="BD.txt"):
	def reading(fisier):
		f=open(fisier,"r")
		linie=f.readline().strip()
		lista={}

		while linie:
			if linie[0]=='[' and linie[len(linie)-1]==']' and linie[1:len(linie)-1] not in lista:
				aux=linie[1:len(linie)-1]
				lista[aux]=[]
			elif linie[0]!='#' and linie[1:len(linie)-1] not in lista:
				lista[aux].append(linie)
			elif linie[0]!='#':
				return("Error !")	#daca nu e comentariu si e o denumire care a fost afisam "Error !"
				sys.exit()
			linie=f.readline().strip()
		return(lista)


	def States(lista):
		multime=[]
		list_of_states={}

		if "States" in lista and lista["States"]!=[]:
			for aux in lista["States"]:
				aux=aux.split(',')
				multime.append(aux)

			for i in multime:
				if 'S' in i and 'S' in list_of_states:
					list_of_states['S'].append(i[0])
				elif 'S' in i:
					list_of_states['S']=[i[0]]
				if 'F' in i and 'F' in list_of_states:
					list_of_states['F'].append(i[0])
				elif 'F' in i:
					list_of_states['F']=[i[0]]
				if 'None' in list_of_states and 'F' not in i and 'S' not in i:
					list_of_states['None'].append(i[0])
				else:
					list_of_states['None']=[i[0]]
		else:
			if 'S' not in list_of_states:
				return("The startup state doesn't exist")
				sys.exit()
			elif 'F' not in list_of_states:
				return("The accept state doesn't exist so answer is Declined")
				sys.exit()
		return(list_of_states)


	def Delta(lista):
		edges_set={}

		for aux in lista['Delta']:
			aux=aux.split(',')

			if aux[0] in edges_set:
				edges_set[aux[0]].append(aux[1])
				edges_set[aux[0]].append(aux[2])
			else:
				edges_set[aux[0]]=[aux[1] , aux[2]]

		return(edges_set)


	def Program_principal(fisier , date_intrare):
		lista = reading(fisier)
		list_of_states = States(reading(fisier))
		edges_set = Delta(reading(fisier))
		current_state=list_of_states['S'][0]
		date_intrare=date_intrare.strip()
		
		for current_input in date_intrare:
			if (current_input not in lista['Sigma']):    #verificam daca in baza de date mai exact in [Sigma] exista inputul
				return("Sigma or input is wrong")
				sys.exit()

			if current_input in edges_set[current_state]:
				for aux_state in range(0,len(edges_set[current_state])-1,+2):
					if current_input==edges_set[current_state][aux_state]:
						current_state=edges_set[current_state][aux_state+1]

		if current_state in list_of_states['F']:
			aux="Accepted"
			return aux
		else:
			aux="Decline"
			return aux


	return Program_principal(fisier , date_intrare)

win=tk.Tk()
win.title("Emulator Automate Finite")
win.configure(width=500 , height=300)
win.minsize(width=500 , height=300)
win.configure(bg='#333333')

#linia de input , box+label
input_label = tk.Label(win, text="Input :" , bg='#333333' , font='Calibri' ,fg='White')
input_label.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)

input_entry =tk.Text(win , bg='#686868' , height=1 , width=40 )

input_entry.grid(
	column=1,
	row=0,
	sticky=tk.E,
	padx=5,
	pady=5,
)
#############


#run button
run_button=tk.Button(
	win,
	text="Start",
	font='Calibri',
	bg='#333333',
	fg='white',
	border=0,
	command=lambda: afis()
).grid(
	column=2,
	row=0,
	padx=5,
	pady=5
)
#############


#linia de outuput , box+label+functia de afisare folosita la butonul de start
output_label = tk.Label(win , text="Output : " , bg='#333333' , font='Calibri' , fg='White')
output_label.grid(column=0 , row=1 , sticky=tk.W , padx=5 , pady=5)

afis_label= tk.Text(win , bg='#333333' , fg='White' , border=0 ,height=1 , width=40 )
afis_label.grid(row=1 , column=1 , sticky=tk.W , padx=5 , pady=5 )

def afis():
	afis_label.delete(1.0,tk.END)
	aux=progr(input_entry.get(1.0 , tk.END))
	afis_label.insert(1.0 , aux)
#############


#exit button
exit_button=tk.Button(
	win,
	text="Exit",
	font='Calibri',
	bg='#333333',
	fg='white',
	border=0,
	command= lambda : win_exit()
).grid(
	row=10,
	column=10,
	sticky=tk.SW
	)
#############


#afisare si modificare de fisier cu text box
file_show= tk.Text(win , bg='#686868' , width=40 , height=20)

file_show.grid(
	row=3,
	column=3
)

file_label = tk.Label(win , text="Date.in" , bg='#333333' , fg='White' , font='Calibri')
file_label.grid(
	row=0,
	column=3,
	sticky=tk.S
)

def afis_fisier(fisier="BD.txt"):
	f=open(fisier , 'r')
	s=f.readline()
	lista=[]
	while s:
		file_show.insert(tk.END , s)
		s=f.readline()
afis_fisier()

bd_button = tk.Button(
	win,
	text="Modify",
	font='Calibri',
	bg='#333333',
	fg='white',
	border=0,
	command=lambda : bd_change()
).grid(
	padx=5,
	pady=5,
	row=1,
	column=3,
	sticky=tk.N
)

def bd_change(fisier="BD.txt"):
	f=open(fisier , "w")
	linie=file_show.get(1.0 , tk.END)
	f.write(linie)

bd_change()
#############

def win_exit():
	sys.exit()

win.after(1)
win.mainloop()