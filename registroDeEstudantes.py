class NoAVL:
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome
        self.altura = 1
        self.esquerda = None
        self.direita = None


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, no):
        if not no:
            return 0
        return no.altura

    def fator_balanceamento(self, no):
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, y):
        x = y.esquerda
        t2 = x.direita

        x.direita = y
        y.esquerda = t2

        y.altura = max(self.altura(y.esquerda),
                        self.altura(y.direita)) + 1
        x.altura = max(self.altura(x.esquerda),
                        self.altura(x.direita)) + 1
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        t2 = y.esquerda

        y.esquerda = x
        x.direita = t2

        x.altura = max(self.altura(x.esquerda),
                       self.altura(x.direita)) + 1
        y.altura = max(self.altura(y.esquerda),
                       self.altura(y.direita)) + 1
        return y

    def inserir(self, no, matricula, nome):
        if not no:
            return NoAVL(matricula, nome)
        if matricula < no.matricula:
            no.esquerda = self.inserir(no.esquerda, matricula, nome)
        elif matricula > no.matricula:
            no.direita = self.inserir(no.direita, matricula, nome)
        else:
            print("Número mecanográfico já existe!")
            return no
        no.altura = 1 + max(self.altura(no.esquerda),
                            self.altura(no.direita))

        fb = self.fator_balanceamento(no)

        if fb > 1 and matricula < no.esquerda.matricula:
            return self.rotacao_direita(no)
        if fb < -1 and matricula > no.direita.matricula:
            return self.rotacao_esquerda(no)
        if fb > 1 and matricula > no.esquerda.matricula:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)
        if fb < -1 and matricula < no.direita.matricula:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)
        return no

    def remover(self, no, matricula):
        if not no:
            return no
        if matricula < no.matricula:
            no.esquerda = self.remover(no.esquerda, matricula)
        elif matricula > no.matricula:
            no.direita = self.remover(no.direita, matricula)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            temp = self.min_valor_no(no.direita)
            no.matricula = temp.matricula
            no.nome = temp.nome
            no.direita = self.remover(no.direita, temp.matricula)
        if no is None:
            return no
        no.altura = 1 + max(self.altura(no.esquerda),
                            self.altura(no.direita))

        fb = self.fator_balanceamento(no)

        if fb > 1 and self.fator_balanceamento(no.esquerda) >= 0:
            return self.rotacao_direita(no)
        if fb > 1 and self.fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)
        if fb < -1 and self.fator_balanceamento(no.direita) <= 0:
            return self.rotacao_esquerda(no)
        if fb < -1 and self.fator_balanceamento(no.direita) > 0:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)
        return no

    def min_valor_no(self, no):
        atual = no
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def pesquisar(self, no, matricula):
        if not no:
            return None
        if no.matricula == matricula:
            return no
        if matricula < no.matricula:
            return self.pesquisar(no.esquerda, matricula)
        return self.pesquisar(no.direita, matricula)

    def imprimir_em_ordem(self, no):
        if no:
            self.imprimir_em_ordem(no.esquerda)
            print(f"Número mecanográfico: {no.matricula} | Nome: {no.nome}")
            self.imprimir_em_ordem(no.direita)

def menu():
    print("\n--------------------------------------")
    print("\t1.Inserir estudante")
    print("\t2.Pesquisar estudante")
    print("\t3.Listar todos os estudantes")
    print("\t4.Remover estudante")
    print("\t0.Sair")
    print("--------------------------------------")


if __name__ == "__main__":

    avl = ArvoreAVL()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            matricula = int(input("Digite o número mecanográfico: "))
            nome = input("Digite o nome: ")
            avl.raiz = avl.inserir(avl.raiz, matricula, nome)
            print("Estudante inserido com sucesso!")

        elif opcao == "2":
            matricula = int(input("Digite o número mecanográfico para a pesquisa: "))
            aluno = avl.pesquisar(avl.raiz, matricula)

            if aluno:
                print(f"Estudante encontrado: {aluno.nome}")
            else:
                print("Estudante não encontrado.")

        elif opcao == "3":
            if avl.raiz is None:
                print("Nenhum estudante cadastrado!.")
            else:
                print("\nLISTA DE ESTUDANTES (EM ORDEM)")
                avl.imprimir_em_ordem(avl.raiz)
        elif opcao == "4":
            matricula = int(input("Digite o número mecanográfico a remover: "))
            avl.raiz = avl.remover(avl.raiz, matricula)
            print("Estudante removido (se existia).")
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida!")
