# SEL0337 - Projetos em Sistemas Embarcados
## Prática 2: Instalação e Configuração de SO em Sistemas Embarcados

**Autores:**
* João Vitor Miranda Sousa — Nº USP: 14802702
* Fernando Shoji Ogusuku — Nº USP: 15636682
* Eduardo Yumoto Carvalheira — Nº USP: 15636160 

---

### 1. Resumo de Hardware e Sistema

**Especificações Técnicas (Baseadas nas saídas de `neofetch` e `pinout`):**
* **Placa:** Raspberry Pi 3 Model B Plus Rev 1.3
* **SoC:** Broadcom BCM2837 / BCM2837B0
* **Arquitetura e CPU:** ARMv8 (aarch64) Quad-Core Cortex-A53 @ 1.40 GHz
* **Memória RAM:** 1 GB LPDDR2 (309 MiB em uso durante a execução)
* **Kernel:** Linux 6.1.54-v8+
* **Conectividade e Interfaces:** Wi-Fi 802.11ac, Bluetooth 4.2, 4x USB 2.0, Ethernet (300 Mbps máximo), 1x CSI (Câmera), 1x DSI (Display), Barramento GPIO de 40 pinos.

**Requisito Fundamental para Execução de Linux Embarcado**
O requisito de hardware indispensável para executar um Sistema Operacional de propósito geral, como o Linux, é a presença da Unidade de Gerenciamento de Memória (MMU - *Memory Management Unit*). A MMU é responsável pela tradução de endereços de memória virtual para física, garantindo o isolamento de processos e a proteção de memória entre o Kernel e o espaço de usuário. Microcontroladores tradicionais (como as famílias ARM Cortex-M ou PIC) não possuem MMU — contando, no máximo, com uma MPU (*Memory Protection Unit*) —, o que os limita à execução de aplicações *bare-metal* ou Sistemas Operacionais de Tempo Real (RTOS) mais restritos.

---

### 2. Fundamentação Teórica

**Questão 1: Análise Comparativa das Gerações da Raspberry Pi (3B+, 4B e 5)**
A Raspberry Pi 3B+ (equipada com o SoC BCM2837B0, Cortex-A53 a 1.4GHz, 1GB de RAM e USB 2.0) atende de forma satisfatória a aplicações embarcadas com requisitos básicos. A geração subsequente, Raspberry Pi 4B, apresentou um avanço significativo com a adoção do SoC BCM2711 (Cortex-A72 a 1.5-1.8GHz), introduzindo opções de memória de 2GB a 8GB LPDDR4, portas USB 3.0, Gigabit Ethernet nativa e saídas Micro-HDMI duplas com suporte a vídeo em 4K. Recentemente, a Raspberry Pi 5 adotou o SoC BCM2712 (Cortex-A76 a 2.4GHz), mais que dobrando a capacidade de processamento. Esta última versão também integrou o chip controlador de I/O RP1 dedicado, interface PCIe 2.0, botão de energia físico e suporte a RTC, mitigando consideravelmente os gargalos de barramento observados nas gerações passadas.

**Questão 2: Comparativo de SoCs (Broadcom em relação ao Mercado)**
O modelo BCM2837B0 opera com 4 núcleos Cortex-A53 (1.4GHz) e GPU VideoCore IV. A evolução para o BCM2711 trouxe 4 núcleos Cortex-A72 (1.5GHz) e GPU VideoCore VI, incorporando barramentos PCIe internos. O modelo atual, BCM2712, avança para 4 núcleos Cortex-A76 (2.4GHz) e GPU VideoCore VII, adicionando suporte a PCIe 2.0 externo.
Ao expandir a comparação para alternativas consolidadas no mercado industrial, destacam-se:
* **TI AM3358 (BeagleBone Black):** Focado em controle industrial de tempo real, possui um núcleo Cortex-A8 (1GHz) operando em conjunto com dois coprocessadores PRU de baixíssima latência.
* **NXP i.MX6 (Módulo Toradex Colibri):** Prioriza a confiabilidade em aplicações automotivas e industriais críticas, empregando núcleos Cortex-A9, barramento CAN integrado nativamente e oferecendo notável longevidade de fornecimento do componente no mercado.

---

### 3. Registros de Execução e Saídas do Terminal

As listagens a seguir apresentam os dados extraídos diretamente da placa durante a execução da prática, documentando o ambiente de hardware e as configurações de rede ativas.

#### 3.1. Informações do Sistema (`fastfetch`)
```text
OS: Debian GNU/Linux 13 (trixie) aarch64
Host: Raspberry Pi 3 Model B Plus Rev 1.3
Kernel: Linux 6.1.54-v8+
Uptime: 50 mins
Packages: 1642 (dpkg)
Shell: bash 5.2.37
CPU: BCM2837 (4) @ 1.40 GHz
GPU: Broadcom bcm2835-vc4 [Integrated]
Memory: 309.32 MiB / 908.54 MiB (34%)
Disk (/): 5.96 GiB / 27.86 GiB (21%) - ext4
Local IP (wlan0): 192.168.1.103/24
```

#### 3.2. Mapa de Hardware (`pinout`)
```text
Description        : Raspberry Pi 3B+ rev 1.3
Revision           : a020d3
SoC                : BCM2837
RAM                : 1GB
Storage            : MicroSD
USB ports          : 4 (of which 0 USB3)
Ethernet ports     : 1 (300Mbps max. speed)
Wi-fi              : True
Bluetooth          : True

 ,--------------------------------.
 | oooooooooooooooooooo J8 PoE +====
 | 1ooooooooooooooooooo   12   | USB
 |  Wi                   oo    +====
 |  Fi  Pi Model 3B+ V1.3         |
 | |D      ,---.          1o   +====
 | |S      |SoC|             RUN | USB
 | |I      `---'                 +====
 | |0                C|             |
 |                   S|        +======
 |                   I| |A|    |   Net
 |pwr      |HDMI|  0| |u|    +======
 `-| |------|    |-----|x|--------'

    3V3  (1) (2)  5V    
  GPIO2  (3) (4)  5V    
  GPIO3  (5) (6)  GND   
  GPIO4  (7) (8)  GPIO14
    GND  (9) (10) GPIO15
 GPIO17 (11) (12) GPIO18
 GPIO27 (13) (14) GND   
 GPIO22 (15) (16) GPIO23
    3V3 (17) (18) GPIO24
 GPIO10 (19) (20) GND   
  GPIO9 (21) (22) GPIO25
 GPIO11 (23) (24) GPIO8 
    GND (25) (26) GPIO7 
  GPIO0 (27) (28) GPIO1 
  GPIO5 (29) (30) GND   
  GPIO6 (31) (32) GPIO12
 GPIO13 (33) (34) GND   
 GPIO19 (35) (36) GPIO16
 GPIO26 (37) (38) GPIO20
    GND (39) (40) GPIO21
```

#### 3.3. Histórico de Comandos Executados (`history`)
```bash
    1  sudo passwd root
    2  clear
    3  sudo passwd root
    4  sudo raspi-config
    5  reboot
    6  sudo raspi-config
    7  reboot
    8  ls
    9  touch pratica2.txt
   10  echo "hello world" > acessossh.txt
   11  sudo rpi-update
   12  sudo apt install neofetch
   13  sudo apt install fastfetch
   14  fastfetch
   15  pinout
   16  ifconfig
   17  history
   18  ls
   19  cd acessossh
   20  cd ~acessossh
   21  cd acessossh
   22  cat acessossh.txt
   23  histoty
   24  history
   25  ls
   26  history
   27  ls
   28  history 
   29  history
   30  ls
   31  clear
   32  sudo poweroff
   33  pinout
   34  python3 --version
   35  pip --version
   36  python3 -m pip install --user virtualenv
   37  sudo apt install python3-venv -y
   38  python3 -m venv 2506
   39  source 2506/bin/activate
   40  cd 2506
   41  pip freeze
   42  pip3 install gpiozero
   43  pip3 install RPi.GPIO
   44  pip3 install lgpio
   45  pip freeze
   46  pip3 install lgpio
   47  nano blink.py
   48  python3 blink.py 
   49  nano blink.py
   50  python3 blink.py 
   51  nano blink.py
   52  python3 blink.py 
   53  nano blink2.py
   54  pip3 install lgpio
   55  pip freeze
   56  python3 blink.py 
   57  ls
   58  nano blink2.py 
   59  python3 blink2.py
   60  nano blink2.py 
   61  nano blink3.py
   62  python3 blink3.py
   63  nano blink3.py
   64  python3 blink3.py
   65  nano blink3.py
   66  python3 blink3.py
   67  nano blink3.py
   68  python3 blink3.py
   69  nano blink3.py
   70  python3 blink3.py
   71  nano blink3.py
   72  python3 blink3.py
   73  nano blink3.py
   74  python3 blink3.py
   75  nano blink3.py
   76  python3 blink3.py
   77  nano blink3.py
   78  python3 blink3.py
   79  nano blink3.py
   80  python3 blink3.py
   81  nano blink3.py
   82  python3 blink3.py
   83  nano blink3.py
   84  python3 blink3.py
   85  nano blink3.py
   86  pip3 install lgpio
   87  cd ..
   88  ifconfig
   89  ls
   90  cat scp-001.txt 
   91  sudo rpi-update cac01bed1224743104cb2a4103605f269f207b1a#6.1.54
   92  ls
   93  2506
   94  cd 2506
   95  ls
   96  scp blink3.py Matheus@192.168.1.104:~/
   97  sudo apt install lgpio
   98  sudo apt install python3-rpi-lgpio
   99  sudo passwd root
  100  sudo raspi-config
  101  reboot
  102  history
  103  sudo poweroff
  104  ls
  105  touch pratica2.txt
  106  nano pratica2.txt
  107  nano histp2.txt
  108  sudo raspi-config
  109  reboot
  110  sudo apt update
  111  sudo apt install neofetch
  112  sudo apt install fastfetch
  113  fastfetch
  114  pinout
  115  sudo apt install pintou
  116  sudo apt install pinout
  117  ifconfig
  118  ip addr
  119  history> historico_comandos.txt
  120  history >> historico_comancaos.txt
  121  cat historico_comandos.txt
  122  fastfetch >> historico_comando
  123  cat historico_comando
  124  fastfetch >> historico_comando.txt
  125  rm historico_comando
  126  cat historico_comando.txt 
  127  history > historico_comando
  128  rm historico_comando
  129  history > historico_comando.txt
```
