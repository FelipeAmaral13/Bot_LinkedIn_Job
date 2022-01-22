# Bot_LinkedIn_Job

Começando
------------
Primeiro, clone o repositório em algum lugar do seu computador ou baixe o arquivo .zip, extraia e navegue até a pasta.
Supondo que você tenha o Python3 instalado, ative um ambiente virtual (opcional) e digite o seguinte comando.

`pip3 install -r requirements.txt`

O modelo de arquivo de configuração é mostrado abaixo.
Você precisará editar isso de acordo com os empregos que está procurando e seus locais.
Você também precisará adicionar suas credenciais do LinkedIn.
Certifique-se de que o arquivo de configuração siga a sintaxe json adequada.

```
{
    "username": "username",
    "password": "password",
    "job_titles": [
        "Engenheiro de dados"
    ],
    "locations": [
        "Brasil"
    ]
}
```