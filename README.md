

# Semaninha Letterboxd


Eu sou adepto desses sites onde voce registra e compartilha as mídias que anda consumindo... lastFM, letterboxd, goodReads... 
e nesse mundo eu me deparei com uma aplicação muito legal >>[tapmusic](https://tapmusic.net/)<< que fazia uma colagem das últimas músicas escutadas por você usando os dados do seu LastFM.


Eu queria ter um meio de compartilhar minha ""semaninha"" de filmes. Sempre achei scraping bem divertido então não foi problema conseguir todos os dados que eu queria,nome do filme, nota do usuário, um url para a imagem do poster . Montei a imagem no backend e criei uma api simples usando FastAPI para servir uma pagina html. E tava feito, aproveitei que tinha uns créditos sobrando na conta de estudante da aws e decidi fazer o deploy da api.


Em outro momento eu descobri um [bot no telegram](https://github.com/wfrancescons/letterboxdgram-bot/tree/main) que fazia exatamente o que eu queria e mais um pouco, eu conversei um pouco com o desenvolvedor do bot e ele me apresentou uma outra opção invés de fazer uma requisição com o selenium para pegar os dados. Ele me introduziu brevemente ao [RSS](https://pt.wikipedia.org/wiki/RSS), e me mostrou que o letterboxd serve essas informações usando o endereço https://letterboxd.com/{username}/rss. E ai foi outro mundo, eu mudei a forma como eu buscava as informações e adotei essa opção, excluindo o serviço do selenium-grid e simplificando o sistema.


Pra terminar a brincadeira e mandar para meus amigos eu comprei um domínio, adicionei um certificado ssl pela aws e foi isso :)

https://chunkysnail.xyz/


ps: É muito provável que quando você estiver tentando acessar receba um 503... provavelmente acabaram os trocados da conta da aws academy ou a sessão do lab pode só ter expirado :/


ps2: Caso queira testar localmente
> `docker-compose up -d`


