

def hover(e):
    if e.data == "true":
        e.control.scale = 1.06
        e.control.opacity = 0.8
    else:
        e.control.scale = 1.0
        e.control.opacity = 1.0

    if e.control.page:  # Garante que o controle foi adicionado à árvore da página
        e.control.update()

def formatar_cpf(e):
    cpf = e.control.value
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
    if len(cpf) > 11:
        cpf = cpf[:11]
    if len(cpf) > 9:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    elif len(cpf) > 6:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
    elif len(cpf) > 3:
        cpf = f"{cpf[:3]}.{cpf[3:]}"
    e.control.value = cpf
    e.control.update()

def formatar_data(e):
    data = e.control.value
    data = ''.join(filter(str.isdigit, data))  # Remove caracteres não numéricos
    if len(data) > 8:
        data = data[:8]
    if len(data) > 4:
        data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
    elif len(data) > 2:
        data = f"{data[:2]}/{data[2:]}"
    e.control.value = data
    e.control.update()
