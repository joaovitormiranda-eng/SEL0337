# SEL0337 — Prática 5 | Checkpoint 1 — Kit de preparação para o laboratório

**Propósito:** criar um serviço `systemd` que inicia automaticamente um blink de LED em Python no boot da Raspberry Pi. Os arquivos ainda **não foram testados na Raspberry física**; verifique a versão do SO, permissões e GPIOs antes de usar.

## Ligações do circuito

- **GPIO18 (BCM) / pino físico 12** → **resistor de 220–330 Ω** → ânodo do LED (perna longa).
- Cátodo do LED (perna curta) → **GND**, por exemplo pino físico 6.
- Mantenha a Raspberry desligada ao realizar as ligações. Verifique polaridade e resistor antes de energizar.

## 1. Diagnóstico inicial, sem alterar o sistema

```bash
cat /etc/os-release | head -8
uname -a
id
command -v python3
python3 -c 'import gpiozero; print("gpiozero OK")'
ls -ld /sys/class/gpio 2>/dev/null || true
systemctl --version | head -1
```

**Não execute** `rpi-update` automaticamente no computador do laboratório: o roteiro sugere um firmware específico e essa operação pode modificar o kernel. Se o professor exigir, peça orientação antes. Nos Raspberry Pi OS modernos, `/sys/class/gpio` é uma interface legada; não force uma atualização do sistema para habilitá-la.

## 2. Teste em Python, ainda sem instalar serviço

Com o LED devidamente conectado, dentro da pasta `checkpoint_1`:

```bash
python3 blink_python.py
```

Verifique que o LED pisca; encerre com `Ctrl+C`. O LED deverá ser desligado na finalização. Se faltar `gpiozero`, informe ao monitor; em muitas imagens Raspberry Pi OS ela já vem instalada. Não instale pacotes globalmente sem autorização.

## 3. Exemplo do roteiro em Bash (GPIO sysfs legado)

Somente se `/sys/class/gpio/export` existir e houver autorização:

```bash
bash -n blink.sh
sudo bash blink.sh
```

Use `Ctrl+C` para interromper. O script tenta desligar o LED e liberar a GPIO que exportou. **Não execute o Bash e o Python ao mesmo tempo**, porque ambos utilizam GPIO18.

## 4. Gerar e instalar a unidade do systemd

O gerador usa o usuário, caminho e interpretador Python da Raspberry. Revise antes de instalar:

```bash
bash gerar_unit.sh
cat sel0337-p5-blink.service
sudo systemd-analyze verify "$(pwd)/sel0337-p5-blink.service"
```

Após conferir os valores `User`, `WorkingDirectory`, `ExecStart` e `ExecStop`, instale:

```bash
sudo cp sel0337-p5-blink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start sel0337-p5-blink.service
systemctl status sel0337-p5-blink.service --no-pager
journalctl -u sel0337-p5-blink.service -n 30 --no-pager
```

Confirme que o LED pisca. Agora teste `stop` e reinício:

```bash
sudo systemctl stop sel0337-p5-blink.service
journalctl -u sel0337-p5-blink.service -n 30 --no-pager
sudo systemctl start sel0337-p5-blink.service
```

O helper `stop_notice.py` é executado via `ExecStop`; **o desligamento do LED é feito por `blink_python.py` ao receber SIGTERM do systemd**. Não é o helper que controla a GPIO.

## 5. Testar o boot (após salvar trabalhos e confirmar com o responsável)

```bash
sudo systemctl enable sel0337-p5-blink.service
systemctl is-enabled sel0337-p5-blink.service
sudo reboot
```

Após a reinicialização, o LED deve piscar automaticamente. Verifique:

```bash
systemctl status sel0337-p5-blink.service --no-pager
journalctl -b -u sel0337-p5-blink.service --no-pager
```

**No equipamento compartilhado:** confirme com o professor se o serviço deve permanecer habilitado; para desabilitá-lo e pará-lo use `sudo systemctl disable --now sel0337-p5-blink.service`. Não exclua unidades nem altere serviços de outras equipes.

## 6. Evidências obrigatórias e úteis

1. Foto da montagem física com o LED, resistor e Raspberry.
2. Captura do teste do programa Python.
3. Captura do serviço ativo no `systemctl status`.
4. Captura do registro `journalctl -b -u ...` após o reboot, e demonstração de que o LED piscou sem comando manual.
5. Captura da parada e da mensagem de `ExecStop`.
6. Para o CP2, em clone Git **na Raspberry**: registrar commits reais e executar `git log > historico_git.txt`.

## 7. Limite da preparação

Os scripts têm verificações estáticas prévias, mas execução física e compatibilidade com GPIO dependem do kit e do Raspberry Pi OS disponível no laboratório. A entrega final do CP2 exige documentação em `README.md` no GitHub e `historico_git.txt` gerado na Raspberry, conforme o roteiro oficial.
