João Vitor Miranda Sousa - 14802702
Fernando Shoji Ogusuku - 15636682
```bash
   58  git branch -M main
   59  # Empurra os arquivos para o GitHub
   60  git push -u origin main
   61  git remote set-url origin https://github.com/joaovitormiranda-eng/SEL0337.git
   62  git push -u origin main
   63  cd 
   64  cd ~
   65  echo "INÍCIO DA PRÁTICA 1"
   66  pwd
   67  mkdir SEL0337
   68  cd SEL0337
   69  pwd
   70  mkdir pratica_1
   71  cd pratica_1
   72  ls
   73  cd pratica_1
   74  nano helloworld.txt
   75  cat helloworld.txt
   76  find . -name '*.txt'
   77  grep -E "14802702|15636682" helloworld.txt
   78  cp helloworld.txt copia.txt
   79  mv copia.txt
   80  rm helloworld.txt
   81  cd
   82  rmdir pratica_1
   83  cd SEL0337/pratica_1
   84  mv copia.txt ..
   85  cd ..
   86  rmdir pratica_1
   87  history | tail -n 30 > README.md
```

---

## 📊 Extras da Prática 1

### 1. Informações do `neofetch`
Ao executar o comando `neofetch` no terminal, o sistema retorna uma arte em ASCII com a logo da distribuição em uso, acompanhada de um resumo rápido do sistema, sendo as principais informações:
* **OS:** A distribuição e versão do sistema operacional Linux.
* **Kernel:** A versão do núcleo do sistema (responsável pela comunicação entre hardware e software).
* **Uptime:** Há quanto tempo o computador está ligado.
* **Shell:** O interpretador de comandos ativo (ex: bash).
* **Hardware:** Resumo do processador (CPU), placa de vídeo (GPU) e uso de memória RAM.

### 2. Significado das Permissões (`ls -l`)
Ao rodar `ls -l /home/sel`, os arquivos e diretórios são listados com uma string de 10 caracteres no início (ex: `-rwxr-xr--` ou `drwxrwxr-x`). O significado é dividido da seguinte forma:
* **1º Caractere (Tipo):** Indica se é um arquivo comum (`-`) ou um diretório/pasta (`d`).
* **Próximos 9 Caracteres (Permissões):** Divididos em 3 blocos de 3 letras (`r` = Read/Ler, `w` = Write/Gravar, `x` = Execute/Executar).
  * **1º Bloco (Owner/Usuário):** Define o que o criador/dono do arquivo pode fazer.
  * **2º Bloco (Group/Grupo):** Define o que os usuários pertencentes ao mesmo grupo podem fazer.
  * **3º Bloco (Others/Outros):** Define o que qualquer outro usuário do sistema pode fazer.
