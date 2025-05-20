# 🗳️ Urna Eletrônica Digital - Streamlit
## 🎯 Objetivo
Criar uma Urna Eletrônica simples, moderna e funcional usando Streamlit para uma interface web interativa, que permita:

📋 Cadastrar candidatos com foto, número, nome e partido

🗳️ Realizar votação com teclado numérico em tela

✅ Confirmar votos válidos, em branco ou nulos

📊 Apresentar resultado final da votação com total de votos e vencedor

Tudo isso com um visual clean, intuitivo e cores inspiradas na bandeira do Brasil 🇧🇷.

⚙️ Funcionalidades
Função	Descrição	Emojis
Cadastro de Candidatos	Permite inserir nome, número, partido e foto do candidato	📝📷
Votação	Voto via botões tipo teclado numérico, mostrando foto do candidato ao digitar número	🔢🗳️
Voto Branco	Botão para registrar voto em branco	⚪
Corrigir Voto	Botão para apagar número digitado e corrigir antes de confirmar	✏️
Contagem de Votos	Soma votos para cada candidato, branco e nulos	🔢
Resultado Final	Exibe relatório completo com votos e declara vencedor	📊🏆
Salvamento local	Salva fotos e pode salvar resultados em arquivo (ex: .txt)	💾

🖼️ Exemplo de Interface
Tela de Cadastro de Candidatos

Campos para número, nome, partido e upload da imagem

Tela de Votação

Teclado numérico com números, botão branco, corrigir, mostrando foto do candidato

Tela de Resultado Final

Lista com os candidatos e votos, e indicação do vencedor

🚀 Como executar
Instale as dependências:

bash
Copiar
Editar
pip install streamlit pillow
Execute o app:

bash
Copiar
Editar
streamlit run main.py
Acesse no navegador o endereço indicado (normalmente http://localhost:8501)

💡 Observações
As imagens dos candidatos são salvas na pasta imagens/ localmente.

Visual pensado para ser limpo e com cores claras (branco amarelado) com inspiração na bandeira do Brasil.

Permite múltiplos votos até encerrar a votação.

Pode ser adaptado para outros contextos eleitorais.

👨‍💻 Desenvolvedor
Projeto criado para fins educacionais e práticos.

Qualquer dúvida ou sugestão, me chame! 🤖✨

