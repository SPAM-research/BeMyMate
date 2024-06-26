# import json
# import re
# """
#    [0] = title
#    [1] = problem_text
#    [2] = notebook
#    [3] = equations
# """
# problems = [
#    [
#        "ABIGAIL",
#        "Abigail tiene cuatro años más que Jonathan. Hace seis años ella tenía el doble de años que él. ¿Cuántos años tiene ahora Abigail?",
#        "x es EDAD ACTUAL DE ABIGAIL, y es EDAD ACTUAL DE JONATHAN, z es EDAD PASADA DE ABIGAIL",
#        "x = y+4",
#    ],
#    [
#        "ÁREA",
#        "Un terreno con forma de cuadrado tiene un lado de 5 metro. ¿Cuál es el área del terreno?",
#        "y es ÁREA",
#        "",
#    ],
#    [
#        "BOTES",
#        "En un club de tenis tienen dos carros con 105 y 287 pelotas, respectivamente. Las van a poner en botes de 7 pelotas para utilizarlas en un torneo. ¿Cuántos botes serán necesarios?",
#        "x es NÚMERO DE BOTES",
#        "",
#    ],
#    [
#        "BOLSAS",
#        "Disponemos de dos contenedores con 396 y 117 kg de patatas, respectivamente. Para su venta, deben envasarse en bolsas que contengan 9 kg. ¿Cuántas bolsas serán necesarias?",
#        "x es NÚMERO DE BOLSAS",
#        "",
#    ],
# ]

# def process_unknown_quantities(quantities):
#    unknown_quantities = []
#    for q in quantities:
#        name = q["name"]
#        description = re.search(r"text=(.*?), language", q["description"]).group(1)
#        unknown_quantities.append({"name": name, "description": description})
#    return unknown_quantities
#
# def process_known_quantities(quantities):
#    known_quantities = []
#    for q in quantities:
#        name = q["name"]
#        description = re.search(r"text=(.*?), language", q["description"]).group(1)
#        value = q["value"]
#        known_quantities.append(
#            {"name": name, "description": description, "value": value}
#        )
#    return known_quantities
#
# def process_graphs(graphs):
#    graph_list = []
#    for g in graphs:
#        path_list = []
#        for p in g["paths"]:
#            match p["type"]:
#                case "Addition":
#                    op = "' + '"
#                case "Subtraction":
#                    op = "' - '"
#                case "Multiplication":
#                    op = "' * '"
#                case "Division":
#                    op = "' / '"
#            path = f"'{p['result']}' = '{op.join(p['nodes'])}'"
#            path_list.append(path)
#        graph_list.append(path_list)
#    return graph_list
#
# problems = open("problems_json", "r").readlines()
#
# for problem in problems[:1]:
#    problem_dict = json.loads(problem)
#    text = problem_dict["text"]
#    known_quantities = problem_dict["knownQuantities"]
#    unknown_quantities = problem_dict["unknownQuantities"]
#    graphs = problem_dict["graphs"]
#    print(process_graphs(graphs))
# quit()

"""
    [0] = text
    [1] = notebook
"""
problems = [
    (
        "Me he comprado un móvil y lo he pagado con 13 billetes de 5 euros y 4 monedas de 1 euro. ¿Cuánto dinero me ha costado?",
        "z es NÚMERO DE BILLETES",
    ),
    (
        "En una maratón participaron 1637 hombres y 1781 mujeres. ¿Cuál fue el total de participantes?",
        "",
    ),
    (
        "Cuatro amigos fueron a comer a un restaurante. Cada menú costaba 37€. ¿Cuánto costó la comida?",
        "x es NÚMERO DE AMIGOS, z es PRECIO DE CADA MENÚ",
    ),
    (
        "Hemos ido 8 amigos a merendar. Cada uno nos hemos comido 3 frutas. ¿Cuántas frutas nos comimos entre todos?",
        "v es NÚMERO DE AMIGOS, x es NÚMERO DE FRUTAS POR PERSONA",
    ),
    (
        "En una panadería venden 755 barras de pan cada día. ¿Cuántas barras venden en 5 días?",
        "b es NÚMERO DE DÍAS, z es NÚMERO DE BARRAS POR DÍA",
    ),
    (
        "Hemos comprado 14 paquetes de cromos. Si en cada paquete había 7 cromos. ¿Cuántos cromos nos han dado?",
        "b es NÚMERO DE PAQUETES",
    ),
    (
        "María José tiene tres granjas en las que gasta 1322 kilos, 556 kilos y 3008 kilos de pienso, respectivamente. ¿Cuántos kilos de pienso gasta en total?",
        "z es PIENSO QUE SE GASTA EN LA SEGUNDA GRANJA, v es PIENSO QUE SE GASTA EN LA TERCERA GRANJA, a es PIENSO QUE SE GASTA EN LA PRIMERA GRANJA",
    ),
    (
        "He comprado 16 platos, pero al llegar a casa me he dado cuenta que necesitaba 24. ¿Cuántos platos me faltan por comprar?",
        "",
    ),
    (
        "El maestro nos ha mandado completar 6 páginas de un cuadernillo. Si en cada hoja hay 3 problemas. ¿Cuántos problemas tendremos que hacer?",
        "v es NÚMERO DE PROBLEMAS POR PÁGINA, w es NÚMERO DE PÁGINAS",
    ),
    (
        "Se van a plantar 32 rosales en un jardín. Si cada rosal cuesta 3 euros. ¿Cuánto dinero costarán todos los rosales?",
        "c es PRECIO DE CADA ROSAL, b es NÚMERO DE ROSALES",
    ),
    (
        "Sin contar la rueda de repuesto. ¿Cuántas ruedas tienen 8 coches?",
        "c es NÚMERO DE RUEDAS POR COCHE",
    ),
    (
        "Trini ha recogido 166 tapones para reciclaje y Fernando 217. ¿Cuántos tapones ha recogido Fernando más que Trini?",
        "v es TAPONES DE FERNANDO",
    ),
    (
        "Un teléfono fijo tiene 12 botones. ¿Cuántos botones harán falta para construir 7 teléfonos?",
        "",
    ),
    (
        "En un tren viajan 234 personas. Sabemos que 107 son hombres. ¿Cuántas mujeres van a bordo del tren?",
        "y es NÚMERO DE HOMBRES",
    ),
    (
        "Hay 26 coches rojos y 47 blancos en una tienda de alquiler de coches. ¿Cuántos coches hay en la tienda?",
        "",
    ),
    (
        "En un huerto había 248 árboles plantados. La propietaria ha plantado 141 más. ¿Cuántos árboles hay ahora en el huerto?",
        "x es ÁRBOLES QUE HABÍA EN EL HUERTO",
    ),
    (
        "Estamos haciendo una colección de 98 cromos. En el álbum ya hemos pegado 81. ¿Cuántos cromos nos faltan para acabar la colección?",
        "w es CROMOS QUE TIENE LA COLECCIÓN, v es CROMOS EN EL ÁLBUM",
    ),
    (
        "En un parque municipal había 17 árboles. El ayuntamiento decidió plantar otros 62. ¿Cuántos árboles hay ahora?",
        "z es ÁRBOLES QUE HABÍA EN PARQUE, u es ÁRBOLES QUE SE DECIDE PLANTAR",
    ),
    (
        "Queremos comprar 65 silbatos. Hemos ido a una tienda en la que sólo nos han podido vender 26 silbatos. ¿Cuántos silbatos nos quedan por comprar?",
        "b es SILBATOS QUE YA HEMOS COMPRADO",
    ),
    (
        "Antonio tenía 87 cromos y le regaló 13 a Pilar. ¿Con cuántos cromos se ha quedado Antonio?",
        "c es CROMOS QUE TENÍA ANTONIO",
    ),
    (
        "Hemos ido a un campamento que dura 26 días. Ya han pasado 18 días. ¿Cuántos días de campamento nos quedan?",
        "",
    ),
    (
        "Ricardo tiene 56 caracoles y regala 31 a Jorge. ¿Con cuántos caracoles se queda Ricardo?",
        "",
    ),
    (
        "En la media maratón de mi pueblo participan 138 atletas. Si 77 ya han llegado a meta. ¿Cuántos atletas faltan por llegar?",
        "",
    ),
    (
        "En un cine se han proyectado dos películas en un día. A la primera película fueron 176 personas y a la segunda 198. ¿Cuántas personas asistieron en total?",
        "",
    ),
    (
        "A mi cumpleaños han venido 25 chicas y 17 chicos. ¿Cuántas chicas había más que chicos?",
        "c es NÚMERO DE CHICOS, w es NÚMERO DE CHICAS",
    ),
    (
        "Una serie de dibujos animados tiene 58 episodios. Si ya hemos visto 26. ¿Cuántos nos faltan por ver?",
        "c es EPISODIOS VISTOS",
    ),
    (
        "Vicente ha repartido el dinero que tenía que traer al colegio en tres bolsillos de su pantalón. Tiene 24€ en el bolsillo delantero de la derecha, 8€ en el izquierdo y en el trasero 13€. ¿Cuánto dinero lleva en total?",
        "c es DINERO EN EL BOLSILLO TRASERO",
    ),
    (
        "Me han comprado una estantería para que guarde mis libros. Tengo 78 libros y ya he guardado 42 libros. ¿Cuántos libros me faltan por colocar?",
        "y es LIBROS QUE YA HE COLOCADO",
    ),
    (
        "Había 354 flores en una floristería. Se han vendido 278 flores. ¿Cuántas flores quedan?",
        "w es FLORES VENDIDAS",
    ),
    (
        "Manuel ha gastado 39€ en una librería, Mercedes 65€ y Catalina 29€. ¿Cuánto dinero han gastado entre los tres?",
        "",
    ),
    (
        "El año pasado había 31 personas apuntadas al club de atletismo. Este año se han apuntado 17 nuevas. ¿Cuántas personas hay apuntadas ahora?",
        "",
    ),
    (
        "Hemos comprado 43 globos para celebrar una fiesta, pero camino de casa se nos han volado 25. ¿Cuántos globos hemos conseguido llevar a casa?",
        "y es GLOBOS QUE HEMOS COMPRADO",
    ),
    (
        "En la visita a una granja, hemos visto 12 ovejas y 27 cabras. ¿Cuántos animales hemos visto?",
        "",
    ),
    (
        "En un centro de adopción de animales solo admiten perros y gatos. Hay 36 perros y 25 gatos. ¿Cuántos animales hay en total?",
        "a es NÚMERO DE GATOS, u es NÚMERO DE PERROS",
    ),
    (
        "En la mesa había 18 pastelitos de chocolate. Me he llevado 7 pastelitos. ¿Cuántos pastelitos quedan?",
        "y es PASTELITOS QUE ME HE LLEVADO, x es PASTELITOS QUE HABÍA",
    ),
    (
        "Ayer leí 43 páginas de un libro. Hoy he leído 23 páginas. ¿Cuántas páginas he leído entre ayer y hoy?",
        "",
    ),
    (
        "David tiene 14 peces en una pecera. Jorge tiene 9 peces más que David. ¿Cuántos peces tiene Jorge?",
        "u es PECES QUE TIENE DAVID",
    ),
    (
        "Carmen tiene 27 películas. Francisco tiene 12 menos que Carmen. ¿Cuántas películas tiene Francisco?",
        "w es PELÍCULAS QUE TIENE CARMEN",
    ),
    (
        "En un centro de acogida animales hay 94 perros y 51 gatos. ¿Cuántos perros hay más que gatos?",
        "",
    ),
    (
        "Mercedes tiene una colección de 39 postales y le traen 25 más. ¿Cuántas postales tiene ahora?",
        "y es POSTALES QUE LE TRAEN, w es POSTALES QUE TENÍA MERCEDES",
    ),
    (
        "Samuel tiene 63 cómics. Si Samuel tiene 18 más que Patricia. ¿Cuántos cómics tiene Patricia?",
        "w es CÓMICS DE MÁS QUE TIENE SAMUEL, a es CÓMICS QUE TIENE SAMUEL",
    ),
    (
        "Teresa tenía 73 cromos de fútbol y cambió a su primo unos cuantos por un cómic. Tras el cambio aún le quedaron 27 cromos. ¿Cuántos cromos dió por el cómic?",
        "",
    ),
    (
        "En una fiesta, hemos gastado 147 vasos rojos y 221 verdes. ¿Cuántos vasos rojos menos que verdes hemos utilizado?",
        "y es VASOS VERDES",
    ),
    (
        "Esta mañana había 52 árboles en un huerto. Ahora hay 93. ¿Cuántos árboles han plantado?",
        "u es ÁRBOLES QUE HAY AL FINAL",
    ),
    (
        "Hace dos años medía 157 cm de altura. Ahora mido 171 cm. ¿Cuántos centímetros he crecido?",
        "y es ALTURA INICIAL, b es ALTURA FINAL",
    ),
    (
        "En un acuario hay 38 delfines. El año pasado había 21. Sabiendo que aún están los que teníamos el año pasado. ¿Cuántos delfines han traído?",
        "v es DELFINES QUE HAY AL FINAL, z es DELFINES QUE HABÍA AL PRINCIPIO",
    ),
    (
        "Un equipo de fútbol tenía 16 puntos a mitad de temporada. Al final de la temporada quedó el penúltimo de la liga con 33 puntos. ¿Cuántos puntos hizo en la segunda parte de la liga?",
        "x es PUNTOS HASTA MITAD TEMPORADA",
    ),
    (
        "Ayer Juan tenía 47 caramelos. Esta mañana Juan le ha dado algunos caramelos a Isabel. Ahora Juan tiene 29 caramelos. ¿Cuántos caramelos le ha dado Juan a Isabel esta mañana?",
        "w es CARAMELOS QUE TENÍA JUAN AYER",
    ),
    (
        "Ahora Carlos tiene 38 cromos. Esta mañana Carlos le ha dado algunos cromos a Ana. Ayer Carlos tenía 63 cromos. ¿Cuántos cromos le ha dado Carlos a Ana esta mañana?",
        "x es CROMOS QUE TIENE CARLOS AHORA, a es CROMOS QUE TENÍA CARLOS AYER",
    ),
    (
        "Esta mañana en un huerto había 282 calabazas. Ahora hay 162. ¿Cuántas calabazas han recogido?",
        "x es CALABAZAS QUE HAY AL FINAL",
    ),
    (
        "La semana pasada tenía 843€ ahorrados. Esta mañana he comprobado que solo me quedan 651€. ¿Cuánto dinero he gastado?",
        "v es DINERO QUE TENÍA LA SEMANA PASADA",
    ),
    (
        "Ayer David tenía 27 bombones. Esta mañana Montse le ha dado algunos bombones a David. Ahora David tiene 53 bombones. ¿Cuántos bombones le ha dado Montse a David esta mañana?",
        "b es BOMBONES QUE TIENE DAVID AHORA, z es BOMBONES QUE TENÍA DAVID AYER",
    ),
    (
        "Ahora Lucas tiene 107 caramelos. Esta mañana Berta le ha dado algunos caramelos a Lucas. Ayer Lucas tenía 23 caramelos. ¿Cuántos caramelos le ha dado Berta a Lucas esta mañana?",
        "z es CARAMELOS QUE TENÍA LUCAS AYER",
    ),
    (
        "Ayer Ricardo le dio 89 cromos a Julia. Ahora, Julia tiene 166 cromos. ¿Cuántos cromos tenía Julia ayer?",
        "b es CROMOS QUE TIENE JULIA AHORA, y es CROMOS QUE RICARDO HA DADO A JULIA ESTA MAÑANA",
    ),
    (
        "Ahora Maite tiene 78 cromos. A primera hora de esta mañana, Pascual le ha dado 35 cromos a Maite. ¿Cuántos cromos tenía Maite ayer?",
        "u es CROMOS QUE PASCUAL HA DADO A MAITE ESTA MAÑANA, x es CROMOS QUE TIENE MAITE AHORA",
    ),
    (
        "Ayer Elena tenía algunas cromos. Esta mañana Elena le ha dado 47 cromos a Rafael. Ahora Elena tiene 38 cromos. ¿Cuántos cromos tenía Elena ayer?",
        "c es CROMOS QUE TIENE ELENA AHORA",
    ),
    (
        "Ahora Carmen tiene 61 bombones. Esta mañana Carmen le ha dado 26 bombones a Ramón. ¿Cuántos bombones tenía Carmen ayer?",
        "u es BOMBONES QUE CARMEN LE HA DADO A RAMÓN ESTA MAÑANA, c es BOMBONES QUE TIENE CARMEN AHORA",
    ),
    (
        "Ahora en un huerto hay plantadas 249 tomateras. Esta mañana temprano se han plantado 165. ¿Cuántas tomateras había ayer?",
        "z es NÚMERO DE TOMATERAS PLANTADAS ESTA MAÑANA, u es NÚMERO DE TOMATERAS QUE HAY AHORA",
    ),
    (
        "Ahora hay 572 calabazas en un huerto. Ayer se recolectaron 322. ¿Cuántas calabazas había ayer antes de la recogida?",
        "y es NÚMERO DE CALABAZAS QUE SE HAN COGIDO",
    ),
    (
        "Ahora el nivel del agua del río es de 418 cm. En los dos últimos días ha descencido 191 cm. ¿Qué altura tenía hace dos dos días?",
        "x es DESCENSO DEL NIVEL DEL AGUA",
    ),
    (
        "Ahora mido 168 cm de altura. En estos tres últimos años he crecido 29 cm. ¿Cuánto medía hace tres años?",
        "",
    ),
    (
        "Roberto tiene 153 caramelos. Ana tiene 36 caramelos. ¿Cuántos caramelos tiene Roberto más que Ana?",
        "u es CARAMELOS QUE TIENE ROBERTO, w es CARAMELOS QUE TIENE ANA",
    ),
    (
        "Un tigre pesa 198 kg y un chital, una especie de ciervo presa habitual de los tigres 82 kg. ¿Cuánto pesa más un tigre que un chital?",
        "a es PESO DE UN TIGRE",
    ),
    (
        "Estrella tiene 44 cromos. José tiene 27 cromos. ¿Cuántos cromos tiene José menos que Estrella?",
        "z es CROMOS QUE TIENE JOSÉ",
    ),
    (
        "Una ballena azul mide 26 metros de largo y un tiburón ballena 12 metros. ¿Cuánto mide un tiburón ballena menos que una ballena azul?",
        "a es LONGITUD DE UNA BALLENA AZUL",
    ),
    (
        "Fina tiene 45 canicas. Pepe tienen 39 canicas más que Fina. ¿Cuántas canicas tiene Pepe?",
        "",
    ),
    (
        "Un hipopótamo come unos 65 kilos de vegetales diariamente. Un elefante africano come unos 125 kilos más que un hipopótamo. ¿Cuántos kilos come un elefante africano?",
        "u es KILOS DE VEGETALES QUE COME UN HIPOPÓTAMO, x es KILOS QUE COME DE MÁS UN ELEFANTE",
    ),
    (
        "Sergio tiene 60 canicas. Paloma tiene 31 canicas menos que Sergio. ¿Cuántas canicas tiene Paloma?",
        "x es CANICAS DE MENOS QUE TIENE PALOMA, v es CANICAS QUE TIENE SERGIO",
    ),
    (
        "Un guepardo alcanza una velocidad de unos 115 kilometros por hora. La gacela Thomson puede conseguir una velocidad en carrera de 36 kilómetros por hora menos que un guepardo. ¿Qué velocidad alcanza una gacela?",
        "",
    ),
    (
        "Julia tiene 53 cromos de la liga de fútbol. Julia tiene 36 cromos más que Antonio. ¿Cuántos cromos de la liga de fútbol tiene Antonio?",
        "z es CROMOS QUE TIENE JULIA",
    ),
    (
        "Un león pesa alrededor de 220 kilos. Si un león pesa 63 kilos más que una leona. ¿Cuánto pesa una leona?",
        "y es PESO DE MÁS DE UN LEÓN",
    ),
    (
        "Sandra tiene 33 figuritas de la Guerra de la Galaxias. Sandra tiene 38 figuritas menos que Carlos. ¿Cuántas figuritas tiene Carlos?",
        "",
    ),
    (
        "Un cachalote pesa 41 toneladas. Si un cachalote pesa 132 toneladas menos que una ballena azul. ¿Cuánto pesa una ballena azul?",
        "a es PESO DE UN CACHALOTE, z es PESO DE MENOS DE UN CACHALOTE",
    ),
    (
        "Ayer Vicente tenía 37 canicas. Esta mañana Alba le ha dado 58 canicas a Vicent. ¿Cuántas canicas tiene Vicent ahora?",
        "c es CANICAS QUE ALBA LE HA DADO A VICENTE ESTA MAÑANA",
    ),
    (
        "Esta mañana Míriam le ha dado 58€ a Andrés. Ayer Andrés tenía 37€. ¿Cuánto dinero tiene Andrés ahora?",
        "v es DINERO QUE TENÍA ANDRÉS AYER",
    ),
    (
        "Ayer Pedro tenía 42 cromos. Esta mañana Pedro le ha dado 17 cromos a Irene. ¿Cuántos cromos tiene Pedro ahora?",
        "",
    ),
    (
        "Esta mañana Juan le ha dado 23€ a Laura. Ayer Juan tenía 78€. ¿Cuánto dinero tiene Juan ahora?",
        "z es DINERO QUE JUAN HA DADO A LAURA ESTA MAÑANA, c es DINERO QUE TENÍA JUAN AYER",
    ),
    (
        "Hemos comprado un coche y hemos pagado 12 recibos de 400€ cada uno. Si el coche cuesta 12800€. ¿Cuánto dinero falta por pagar?",
        "v es PRECIO DEL COCHE, w es VALOR DE UN RECIBO",
    ),
    (
        "El lince ibérico es una especie en peligro de extinción. En el año 2007, el lince ibérico solo se podía encontrar en Sierra Morena y en Doñana. En ese momento solo quedaban 250 ejemplares. Si sabemos que 53 habitaban en Sierra Morena. ¿Cuántos linces ibéricos vivían en Doñana?",
        "v es NÚMERO DE LINCES EN SIERRA MORENA, c es POBLACIÓN TOTAL DE LINCES",
    ),
    (
        "Desde el año 2000, han muerto en Doñana 24 linces atropellados y 133 por otras causas. ¿Cuántos linces han muerto en Doñana desde el año 2000?",
        "",
    ),
    (
        "Para evitar la desaparición del Lince se han puesto en marcha medidas de protección. En 2002 el número de linces en Andalucía era de 94 y en 2017 de 448 linces. ¿En cuánto aumentó el número de linces entre 2002 y 2017?",
        "x es NÚMERO DE LINCES EN 2002",
    ),
    (
        "El emperador romano Adriano, uno de los Cinco Buenos Emperadores, nació en el año 76 y murió con 62 años. ¿En qué año falleció?",
        "u es AÑO DE NACIMIENTO DE ADRIANO, y es EDAD QUE ADRIANO TENÍA CUANDO MURIÓ",
    ),
    (
        "La persona más longeva de la historia vivió 122 años. Si murió en el año 1997. ¿En qué año nació?",
        "z es AÑO DE FALLECIMIENTO, u es EDAD QUE TENÍA CUANDO MURIÓ",
    ),
    (
        "La ballena azul es el animal más grande que ha habitado el planeta Tierra. Durante mucho tiempo fueron cazadas hasta casi la extinción. En 1911 había unas 200000 ballenas azules en el mundo. Actualmente, se estima que hay unas 25000. ¿En cuántos ejemplares ha disminuido la población de ballenas azules?",
        "z es NÚMERO DE BALLENAS AZULES EN 1911",
    ),
    (
        "En el año 1985 había unos 1500 linces en España. Desde 1960 hasta 1985el número de linces disminuyó en 3500 ejemplares. ¿Cuántos linces había en 1960?",
        "w es DISMINUCIÓN DEL NÚMERO DE LINCES",
    ),
    (
        "En 1970 quedaban en el mundo unos 1000 tigres de Sumatra. Desde ese año hasta 1992 la población se redujo en 600 ejemplares. ¿Cuántos tigres de Sumatra quedaban en 1992?",
        "",
    ),
    (
        "En una empresa, la probabilidad de que un trabajador elegido al azar sea mujer es 0,55. De entre las mujeres, la probabilidad de que esa trabajadora se dedique a tareas administrativas es 0,2. Sabemos también que, del total de trabajadores, la probabilidad de ser hombre y realizar trabajos administrativos es 0,1125. Calcula la probabilidad de ser mujer y no realizar tareas administrativas. [Utiliza la notación A = ser mujer y B = realizar tareas administrativas.]",
        "z es p(A) PROBABILIDAD DE SER MUJER, y es p(B/A) PROBABILIDAD DE REALIZAR TAREAS ADMINISTRATIVAS SABIENDO QUE ES MUJER",
    ),
    (
        "Una clase de primaria está formada por chicos y chicas. De entre los estudiantes, la probabilidad de ser chica y usar gafas es 0,15 mientras que la de ser chica pero no usarlas es 0,37. Además, la probabilidad de ser chico y no usar gafas es de 0,35. De entre los que usan gafas. ¿Qué probabilidad hay de ser chica? [Utiliza la notación A = ser chica y B = llevar gafas.]",
        "x es p(E) PROBABILIDAD DEL SUCESO SEGURO, c es p(noAynoB) PROBABILIDAD DE NO SER CHICA Y NO LLEVAR GAFAS, v es p(AyB) PROBABILIDAD DE SER CHICA Y LLEVAR GAFAS, u es p(AynoB) PROBABILIDAD DE SER CHICA Y NO LLEVAR GAFAS",
    ),
    (
        "Un dispositivo comprueba si una pieza de un móvil es correcta o defectuosa. Se toma una muestra de piezas recién fabricadas y se prueba con el dispositivo si son correctas o defectuosas. La probabilidad de que una pieza tomada al azar sea correcta es 0,95. Sabemos que la probabilidad de que el dispositivo califique una pieza como correcta es 0,77. Además, la probabilidad de que el dispositivo califique como defectuosa una pieza defectuosa es del 0,04. Entre las piezas calificadas como correctas por el dispositivo. ¿Qué probabilidad hay de que sean piezas correctas? [Utiliza la notación A = ser una pieza correcta y B = ser una pieza calificada como correcta por el dispositivo.]",
        "z es p(noAynoB) PROBABILIDAD DE QUE LA PIEZA NO SEA CORRECTA Y NO SEA CALIFICADA COMO CORRECTA POR EL DISPOSITIVO",
    ),
    (
        " En una academia de idiomas, la probabilidad de que un alumno estudie inglés y francés es 0,3. Por otro lado, la probabilidad de que un alumno estudie inglés pero no francés es 0,3. Además, sabemos que la probabilidad de que un alumno estudie francés, sabiendo que no estudia inglés es 0,4. Calcula la probabilidad de que un alumno estudie inglés sabiendo que estudia francés. [Utiliza la notación A = estudiar inglés y B = estudiar francés.]",
        "u es p(B/noA) PROBABILIDAD DE ESTUDIAR FRANCÉS SABIENDO QUE NO ESTUDIA INGLÉS, a es p(AynoB) PROBABILIDAD DE ESTUDIAR INGLÉS PERO NO FRANCÉS",
    ),
    (
        "Un camión ha cargado dos paquetes de 2000 kilos cada uno y 15 paquetes de 500 kilos cada uno. ¿Cuánto pesa la carga en total?",
        "b es NÚMERO DE PAQUETES DE 2000 KILOS, u es PESO DEL PAQUETE DE 500 KILOS",
    ),
    (
        "¿Cuántas botellas de 3/4 de litro se pueden llenar con el contenido de un depósito de 3000 litros de zumo?",
        "w es LITROS DE ZUMO EN EL DEPÓSITO",
    ),
    (
        "Enrique tiene 127 libros. Carla tiene 49 menos que Enrique. ¿Cuántos libros tiene Carla?",
        "b es LIBROS QUE TIENE ENRIQUE",
    ),
    (
        "Matilde ha comprado en unos grandes almacenes un libro y un videojuego. El libro costaba 17€ y el videojuego 69€. Si ha vuelto a casa con 103€. ¿Cuánto dinero llevaba al salir de casa?",
        "b es PRECIO DEL VIDEOJUEGO, c es PRECIO DE UN LIBRO, v es DINERO TIENE AL VOLVER A CASA",
    ),
    (
        "Vicente tiene 4 cajas con 16 chocolatinas cada una. Si Bernardo tiene 5 cajas más que Vicente. ¿Cuántas chocolatinas tiene Bernardo?",
        "w es NÚMERO DE CHOCOLATINAS POR CAJA",
    ),
    ("Pedro tiene 64 bombones en 8 cajas. ¿Cuántos bombones hay en cada caja?", ""),
    (
        "Pascual tiene 114 cómics. Pascual tiene 63 más que Alberto. ¿Cuántos cómics tiene Alberto?",
        "v es CÓMICS QUE TIENE PASCUAL",
    ),
    (
        "Disponemos de dos contenedores con 396 y 117 kg de patatas, respectivamente. Para su venta, deben envasarse en bolsas que contengan 9 kilos. ¿Cuántas bolsas serán necesarias?",
        "z es KILOS DE PATATAS EN EL CONTENEDOR QUE MÁS TIENE",
    ),
    (
        "Vicente compró ayer 21 botellas grandes de refresco y hoy ha comprado 9. Si cada botella cuesta 2 euros. ¿Cuánto ha gastado en total?",
        "u es PRECIO DE UNA BOTELLA",
    ),
    (
        "Un colegio ha comprado 34 ordenadores a 337€ cada uno y 15 pizarras digitales a 1260€ cada una. ¿Cuánto dinero se ha gastado en la compra?",
        "w es PRECIO DE UN ORDENADOR, y es NÚMERO DE ORDENADORES, c es PRECIO DE UNA PIZARRA, z es NÚMERO DE PIZARRAS",
    ),
    (
        "El encargado de un tienda de informática compró 75 impresoras a 47€ cada una. Vendió las 52 primeras a 65€ y el resto a 55€. ¿Qué ganancia obtuvo?",
        "",
    ),
    (
        "El tren nocturno que va de Barcelona a Granada está formado por una locomotora de 11 metros y 17 vagones para pasajeros de 9 metros cada uno. \n\t\t(a) ¿Cuánto miden todos los vagones juntos? \n\t\t(b) ¿Cuánto mide el tren en total?",
        "u es LONGITUD DE UN VAGÓN",
    ),
    (
        "El tren nocturno que va de Barcelona a Granada está formado por una locomotora de 11 metros y 17 vagones para pasajeros de 9 metros cada uno. ¿Cuánto mide el tren en total?",
        "a es LONGITUD DE UN VAGÓN, c es LONGITUD DE LA LOCOMOTORA",
    ),
    (
        "Se compró una cierta cantidad de metros de tela para cortinas, pagándose 528€. Si se hubiesen comprado 12 metros más, se habría pagado 564€. ¿Cuántos metros de tela se compraron?",
        "c es PRECIO REAL DE LAS CORTINAS, b es METROS DE MÁS QUE EN EL CASO IMAGINARIO",
    ),
    (
        "Para ir a la final de copa, un equipo de fútbol ha llenado 14 trenes con 450 plazas cada uno y 106 autobuses con 50 plazas cada uno. Si en cada fila del estadio donde se jugará la final caben 25 personas, ¿cuántas filas se ocuparán en total?",
        "x es NÚMERO DE AUTOBUSES, v es NÚMERO DE PERSONAS EN CADA AUTOBÚS, w es NÚMERO DE PERSONAS QUE CABEN EN UNA FILA, z es NÚMERO DE TRENES, b es NÚMERO DE PERSONAS EN CADA TREN",
    ),
    (
        "Se disponen de 200 metros de tela para hacer 20 trajes que necesitan 3 metros de tela cada uno. El resto de la tela se utilizará para hacer abrigos. Si para hacer cada abrigo se necesitan 4 metros de tela. ¿Cuántos abrigos pueden hacerse?",
        "",
    ),
    (
        "En una granja se gastan todos los días 150 kilos de pienso y 20 kilos de heno para alimentar a los animales. El kilo de pienso cuesta 3€ y el de heno 4€. Si el dinero que pueden gastar en un año es de 200,75 euros. ¿Cuánto dinero sobrará?",
        "b es DÍAS EN UN AÑO",
    ),
    (
        "Un supermercado ha pagado 2720€ por la compra de unas botellas de aceite a las empresas BuenAceite y RicoRico. A la empresa BuenAceite le compró 450 botellas y a la empresa RicoRico 230 botellas. Sabiendo que, el precio de una botella de BuenAceite es el mismo que el de RicoRico. ¿Cuánto dinero recibió la empresa BuenAceite?",
        "w es DINERO TOTAL PAGADO, a es NÚMERO DE BOTELLAS COMPRADAS A BUENACEITE",
    ),
    (
        "Hemos comprado un coche que cuesta 31200€. Si ya hemos pagado 16 recibos de 520€.¿Cuánto dinero falta por pagar?",
        "c es NÚMERO DE RECIBOS QUE YA SE HAN PAGADO, v es PRECIO DEL COCHE, u es VALOR DE UN RECIBO",
    ),
    (
        "Un granjero se dedica a la venta de los huevos que ponen sus gallinas. En la granja tiene 12 corrales grandes y 28 corrales pequeños. Cada corral grande produce 300 huevos diarios y cada corral pequeño 180. Si el granjero vende los huevos en cajas donde caben 60 huevos. ¿Cuántas cajas necesita diariamente?",
        "x es NÚMERO DE HUEVOS DIARIOS QUE PRODUCE UN CORRAL GRANDE, z es NÚMERO DE CORRALES GRANDES",
    ),
    (
        "Un mayorista compra en un matadero 55 corderos a 46 euros cada uno. Vende 33 corderos a un restaurante a 65 euros cada uno y el resto a un supermercado por 58 euros cada uno. ¿Qué beneficio obtuvo?",
        "u es PRECIO AL QUE VENDE CADA CORDERO AL SUPERMERCADO",
    ),
    (
        "Un granjero gasta diariamente 15 kilos de pienso para gallinas y 120 kilos de pienso para vacas. El kilo de pienso para gallinas cuesta 2€ y el de pienso para vacas 5€. Si en un año sólo puede gastar 292000€. ¿Cuánto dinero le sobra?",
        "z es KILOS DIARIOS DE PIENSO PARA GALLINAS, a es PRECIO DE UN KILO DE PIENSO PARA VACAS, y es DINERO DISPONIBLE PARA GASTAR AL AÑO, v es KILOS DIARIOS DE PIENSO PARA VACAS, b es DÍAS EN UN AÑO, x es PRECIO DE UN KILO DE PIENSO PARA GALLINAS",
    ),
    (
        "Un tendero compra 276 huevos en una granja, pero durante el transporte se le rompen 24. Decide vender los que han quedado en envases de 6 huevos. Calcula:\n\t\t a) ¿Cuántos huevos quedan sin romper?\n\t\t b) ¿Cuántos envases necesitará?",
        "",
    ),
    (
        "Un tendero compra 276 huevos en una granja, pero durante el transporte se le rompen 24. Decide vender los que han quedado en envases de 6 huevos. ¿Cuántos envases necesitará?",
        "b es NÚMERO DE HUEVOS ROTOS, w es NÚMERO DE HUEVOS POR ENVASE, a es NÚMERO DE HUEVOS COMPRADOS",
    ),
    (
        "Carla, Itziar y Rodrigo son propietarios de una empresa que este año ha ganado 18000€. Deciden repartir el dinero de forma que a Carla le toquen 6 partes, a Icíar 9 partes y a Rodrigo 5 partes. ¿Cuánto dinero debe recibir cada uno?",
        "a es DINERO QUE RECIBEN DE LA EMPRESA, x es NÚMERO DE PARTES QUE LE CORRESPONDE A RODRIGO, y es NÚMERO DE PARTES QUE LE CORRESPONDE A ITZIAR, c es NÚMERO DE PARTES QUE LE CORRESPONDE A CARLA",
    ),
    (
        "Una imprenta necesita comprar tinta por un valor de 2120€ y 40 cajas de papel a 35€ cada una. Si se dispone de 3500€. ¿Cuánto dinero faltará?",
        "x es PRECIO DE LA TINTA, u es NÚMERO DE CAJAS DE PAPEL, y es DINERO DISPONIBLE",
    ),
    (
        "Para la inauguración de una montaña rusa de un parque de atracciones han llegado 56 autobuses llenos con 45 personas cada uno y 168 coches con sus 5 plazas ocupadas. Si en cada viaje de la montaña rusa caben 42 personas. ¿Cuántos viajes serán necesarios para que suban todos a la atracción?",
        "v es NÚMERO DE PERSONAS QUE SUBEN EN UN VIAJE, w es NÚMERO DE PERSONAS EN CADA COCHE, y es NÚMERO DE COCHES, b es NÚMERO DE AUTOBUSES",
    ),
    (
        "La recaudación obtenida un sábado por los billetes de los 275 viajeros de un tren ha sido 8800€. Si sabemos que el domingo viajaron 15 personas menos y que un billete cuesta 4€ más que el sábado, calcula:\n\t  \t a) ¿Cuánto personas viajaron el domingo? \n\t  \t b) ¿Cuánto cuesta un billete los sábados? \n\t  \t c) ¿Cuánto cuesta un billete los domingos? \n\t  \t d) ¿Cuánto dinero se recaudó domingo?",
        "w es PRECIO DE MÁS POR BILLETE EL DOMINGO, z es NÚMERO DE VIAJEROS EL SÁBADO, c es RECAUDACIÓN DEL SÁBADO, x es NÚMERO DE VIAJEROS DE MENOS EL DOMINGO RESPECTO AL SÁBADO",
    ),
    (
        "La recaudación obtenida un sábado por los billetes de los 275 viajeros de un tren ha sido 8800 euros. Si sabemos que el domingo viajaron 15 personas menos y que un  billete cuesta 4 euros más que el sábado. ¿Cuánto dinero se recaudó domingo?",
        "",
    ),
    (
        "Disponemos de 123 paquetes de almendras de 5 kilos cada uno. Si el precio de un kilo de almendras es de 2€. Calcula:\n\t\ta) ¿Cuál sería el precio de un paquete?\n\t\tb) ¿Cuál sería el precio de todos lo paquetes?",
        "",
    ),
    (
        "¿Cuál es el precio total de 123 paquetes de almendras de 5 kilos cada uno?. Si el precio de un kilo de almendras es de 2€?",
        "",
    ),
    (
        "Ayer fui al banco y saqué 13 billetes. Hoy he sacado 9. Si todos los billetes eran de 5€. ¿Cuánto dinero he sacado del banco en total?",
        "w es NÚMERO DE BILLETES QUE SAQUÉ AYER, v es VALOR DE CADA BILLETE",
    ),
    (
        "Un camión que hace la ruta Madrid Valencia ha cargado una caja de 235 kilos y 26 sacos de 14 kilos. ¿Cuánto pesa la carga en total?",
        "",
    ),
    (
        "Una discoteca ha comprado 52 altavoces a 423€ cada uno y 25 pantallas de TV a 1840€ cada una. ¿Cuánto dinero se ha gastado en total?",
        "x es PRECIO DE UN ALTAVOZ, y es NÚMERO DE PANTALLAS, w es NÚMERO DE ALTAVOCES",
    ),
    (
        "El presupuesto para una fiesta de cumpleaños es de 900€. A la fiesta acudirán 25 niños y el precio del menú es de 12€ por persona. El resto del presupuesto de la fiesta se destinará a pagar a las personas que van a actuar en la fiesta (p. ej., músicos o payasos). Si cada una de estas personas cobran 30 euros por actuar. ¿Cuántas personas se podrían contratar?",
        "c es GASTO PRESUPUESTADO PARA LA FIESTA, w es PRECIO DEL MENÚ POR PERSONA",
    ),
    (
        "Se disponen de 450 metros de tela para hacer 25 disfraces de león que necesitan 6 metros de tela cada uno. El resto de la tela se utilizará para hacer disfraces de elefante. Si para hacer un disfraz de elefante se necesitan 15 metros de tela. ¿Cuántos disfraces de elefante podrán hacerse?",
        "",
    ),
    (
        "He vendido 750 litros de aceite a un precio de 4€ el litro. Con el dinero que he obtenido de la venta, he comprado 120 kilos de cerezas a 2€ el kilo. ¿Cuánto dinero me queda?",
        "",
    ),
    (
        "En la carnicería, hemos comprado 3 kilos de carne de ternera a 13€ el kilo y carne de cordero por valor 26 euros. He pagado con dos billetes de 50€. ¿Cuánto dinero me han devuelto?",
        "c es PRECIO DE UN KILO DE TERNERA, z es NÚMERO DE BILLETES",
    ),
    (
        "De la cosecha de este año un bodeguero ha embotellado 1577 botellas de vino. Si se han vendido 1089. ¿Cuántas botellas le quedan?",
        "",
    ),
    (
        "En una fiesta se van a repartir 4480 globos. Los globos viene almacenados en cajas. Si se han gastado 21 cajas de globos y aún quedan 11 por gastar. Calcula:\n\t\t\t\t\ta) ¿Cuántas cajas de globos había en total? \n\t\t\t\t\tb) ¿Cuántos globos hay en cada caja?",
        "c es NÚMERO DE CAJAS QUE QUEDAN POR GASTAR, y es NÚMERO DE GLOBOS PARA REPARTIR, b es NÚMERO DE CAJAS GASTADAS",
    ),
    (
        "En una fiesta se van a repartir 4480 globos. Los globos viene almacenados en cajas. Si se han gastado 21 cajas de globos y aún quedan 11 por gastar. ¿Cuántos globos hay en cada caja?",
        "",
    ),
    (
        "Vicente compró ayer 21 botellas grandes de refresco y hoy ha comprado 9. Si cada botella cuesta 2 euros. ¿Cuánto ha gastado en total?",
        "z es PRECIO DE UNA BOTELLA, x es NÚMERO DE BOTELLAS QUE COMPRÓ HOY",
    ),
    (
        "Antonio ha comprado 240 naranjas en dos sacos. En un saco hay 70 naranjas más que en el otro. ¿Cuántas naranjas hay en cada saco?",
        "c es NÚMERO DE NARANJAS QUE HAY DE MÁS EN UN SACO, y es NÚMERO DE SACOS, a es NÚMERO DE NARANJAS QUE COMPRA",
    ),
    (
        "Abigail tiene cuatro años más que Jonathan. Hace seis años ella tenía el doble de años que él. ¿Cuántos años tiene ahora Abigail?",
        "b es TIEMPO TRANSCURRIDO, x es AÑOS QUE TIENE ABIGAIL MÁS QUE JONATHAN, c es DOS",
    ),
    (
        "Disponemos de dos tipos de té: uno de Tailandia a 5,2 euros por Kg y otro de la India a 6,2 euros per Kg. ¿Cuántos kilógramos de té de la India tenemos que añadir a 45 kilos de té de Tailandia para obtener una mezcla a 5,75 euros por Kg?",
        "u es PRECIO DE UN KILO DE TÉ DE TAILANDIA, w es KILOS DE TÉ DE TAILANDIA, y es PRECIO DE UN KILO DE TÉ MEZCLADO, z es PRECIO DE UN KILO DE TÉ DE LA INDIA",
    ),
    (
        "Dafne y Fabiola vendieron 124 boletos para un concierto de jazz. Si el número de boletos que vendió Fabiola fue el triple de los que vendió Dafne. ¿Cuántos boletos ha vendido cada una?",
        "w es TOTAL DE BOLETOS VENDIDOS",
    ),
    (
        "Un pintor tiene que pintar una fachada de una finca y planifica que debe pintar 12 metros cuadrados al día para acabar en el plazo previsto. Si pintase 42 metros cuadrados cada día tardaría 25 días menos. ¿Cuántos metros cuadrados tiene la fachada?",
        "z es METROS CUADRADOS DIARIOS A PINTAR EN LA PLANIFICACIÓN INICIAL, y es METROS CUADRADOS DIARIOS A PINTAR EN LA SITUACIÓN HIPOTÉTICA, v es DÍAS QUE TARDARÍA MENOS EN LA SITUACIÓN HIPOTÉTICA",
    ),
    (
        "Se dispone de tela de lana y de tela de algodón. En total 12 metros. El precio del metro de lana es de 2 euros y el de algodón, de 4 euros. El valor total de la tela que se dispone es de 32 euros. ¿De cuántos metros de tela de lana y de cuántos metros de tela de algodón se dispone?",
        "",
    ),
    (
        "Esta mañana he vendido 28 sacos de carbón. Por la tarde solo he vendido 14. Si cada saco cuesta 3 euros. ¿Cuanto dinero he recibido por la venta?",
        "c es PRECIO DE CADA SACO, u es NÚMERO DE SACOS DE CARBÓN VENDIDOS POR LA TARDE",
    ),
    (
        "Un equipo ciclista necesita comprar un automóvil para el jefe del equipo por un valor de 15238 euros y 32 bicicletas a 1135 euros cada una. Si el equipo dispone de 48000 euros. ¿Cuánto dinero faltará?",
        "y es DINERO DISPONIBLE, u es PRECIO DEL COCHE, w es PRECIO DE UNA BICICLETA",
    ),
    (
        "En un almacén guardan 450 cajas de champiñones en dos cámaras frigoríficas. En una cámara hay 80 cajas más que en la otra. ¿Cuantas cajas hay en cada cámara frigorífica?",
        "a es NÚMERO DE CAJAS",
    ),
    (
        "En un gran supermercado han puesto a la venta 89 botes de pimiento en conserva de 3 kilos cada uno. Si el precio de un kilo de pimiento en conserva es de 7 euros. ¿Cual será el precio de todos los botes?",
        "",
    ),
    (
        "Una imprenta ha pagado 1700 euros por la compra de paquetes de papel a las empresas Papeleras del Norte y CompactPapel. Sabemos que a Papeleras del Norte le compró 205 paquetes y a CompactPapel, 135. Si Papeleras del Norte y CompactPapel venden los paquetes de papel al mismo precio. ¿Cuánto dinero recibió la empresa Papeleras del Norte?",
        "",
    ),
    (
        "En un club de tenis disponen de 204 pelotas. Durante una jornada se pierden 18 pelotas. Si las pelotas se guardan en botes de 6 pelotas. ¿Cuántos botes se necesitarán?",
        "",
    ),
    (
        "En una planta embotelladora de bebidas se producen 876 botellas diarias de zumo. Las botellas se empaquetan en cajas de 12 unidades. Si cada caja se vende a 36 euros. ¿Cuánto dinero obtiene la empresa por la venta de la producción diaria?",
        "w es NÚMERO DE BOTELLAS PRODUCIDAS DIARIAMENTE, v es PRECIO DE UNA CAJA",
    ),
    (
        "Una tienda de deportes ha hecho un pedido de 15 bicicletas de montaña a 125€ cada una y 9 bicicletas de carretera a 370€ cada una. Calcula:\n\t\t a) ¿Cuánto han costado las bicicletas de montaña en total?  \n\t\t b) ¿Cuánto han costado las bicicletas de carreteras en total? \n\t\t c) ¿Cuánto ha costado el pedido?",
        "b es NÚMERO DE BICICLETAS DE CARRETERA, u es NÚMERO DE BICICLETAS DE MONTAÑA",
    ),
    (
        "Una tienda de deportes ha hecho un pedido de 15 bicicletas de montaña a 125€ cada una y 9 bicicletas de carretera a 370€ cada una. ¿Cuánto dinero ha costado el pedido?",
        "w es PRECIO DE UNA BICICLETA DE CARRETERA",
    ),
    (
        "Carla y Rodrigo son propietarios de una empresa que este año ha ganado 18000 euros. Deciden repartir el dinero de forma que a Carla le toquen 6 partes y a Rodrigo 9 parts. ¿Cuánto dinero debe recibir cada uno?",
        "c es TOTAL DE DINERO GANADO",
    ),
    (
        "El presupuesto para una fiesta de cumpleaños es de 900 euros. A la fiesta acudirán 25 niños y el precio del menú por persona es de 12 euros. El resto del presupuesto de la fiesta se destinará a pagar a las personas que van a actuar en la fiesta (p. ej., músicos o payasos). Si cada una de estas personas cobran 30 euros por actuar. ¿Cuántas personas se podrían contratar?",
        "",
    ),
    (
        "Tengo que leerme un libro de 237 páginas en tres días. El primer día he leído 24 páginas y el segundo 3 veces más que el primero. \n\t (a) ¿Cuántas páginas leí el segundo día? \n\t (b) ¿Cuántas páginas leí entre el primer y segundo día? \n\t (c) ¿Cuántas páginas tendré que leer el tercer día?",
        "y es NÚMERO DE PÁGINAS LEÍDAS EL PRIMER DÍA, c es NÚMERO DE PÁGINAS DEL LIBRO",
    ),
    (
        "Un almacenista de fruta compra las manzanas a 48 euros la caja y las vende a 6 euros el kilo. Sabiendo que una caja contiene 12 kg. \n\t\t\t\t(a) ¿Cuál es el precio de una caja de fruta? \n\t\t\t\t(b) ¿Cuál es el beneficio que obtiene el almacenista por caja? \n\t\t\t\t(c) ¿Cuántas cajas ha de vender para ganar 600 euros?",
        "c es PRECIO DE VENTA DE UN KILO DE MANZANAS, y es KILOS DE MANZANAS EN UNA CAJA, u es BENEFICIO TOTAL, x es PRECIO DE COMPRA DE UNA CAJA",
    ),
    (
        "Han transportado a una granja un rebaño de ovejas usando 16 camiones con 52 ovejas cada uno. Si las ovejas se van a ubicar en corrales de 104 plazas, calcula: \n\t (a) ¿Cuántas ovejas se han transportado en total? \n\t (b) ¿Cuántos corrales habrá en la granja?",
        "w es NÚMERO DE CAMIONES, x es NÚMERO DE OVEJAS POR CAMION, c es NÚMERO DE OVEJAS POR CORRAL",
    ),
    (
        "Han transportado a una granja un rebaño de ovejas usando 16 camiones con 52 ovejas cada uno. Si las ovejas se van a ubicar en corrales de 104 plazas. ¿Cuántos corrales habrá en la granja.",
        "",
    ),
    (
        "Este año el libro de matemáticas cuesta 2€ menos que el año pasado. Por 18 libros se ha pagado 630€ este año. \n\t\t\t(a) ¿Cuánto cuesta un libro de matemáticas este año? \n\t\t\t(b) ¿Cuánto costaba un libro de matemáticas el año pasado?",
        "w es PRECIO DE MENOS DE UN LIBRO ESTE AÑO, y es NÚMERO DE LIBROS, c es PRECIO DE TODOS LOS LIBROS ESTE AÑO",
    ),
    (
        "Este año el libro de matemáticas cuesta 2€ menos que el año pasado. Por 18 libros se ha pagado 630€ este año. ¿Cuánto costaba un libro de matemáticas el año pasado?",
        "c es PRECIO DE TODOS LOS LIBROS ESTE AÑO",
    ),
    (
        "En una fábrica de piensos se han comprado 2800 kilos de cereales. Sabemos que se han recibido 400 kilos menos de cebada que de trigo y que una quinta parte del envío era de cebada. \n\t\t(a) ¿Cuántos kilos de cebada se han recibido? \n\t\t(b) ¿Cuántos kilos de trigo se han recibido?",
        "c es CINCO, v es PESO DE LOS CEREALES, w es CINCO",
    ),
    (
        "En una fábrica de piensos se han comprado 2800 kilos de cereales. Sabemos que se han recibido 400 kilos menos de cebada que de trigo y que una quinta parte del envío era de cebada. ¿Cuántos kilos de trigo se han recibido?",
        "z es CINCO, x es CINCO",
    ),
    (
        "En un colegio hay 180 estudiantes en quinto de primaria. Se necesita comprar un ejemplar de un libro de lectura para cada estudiante. Cada ejemplar cuesta 25 euros, pero nos hacen un descuento de 20 euros por cada 10 ejemplares que compramos. \n\t\t(A)¿Cuál es el precio de todos los libros sin descuento? \n\t\t(b)¿Cuántos descuentos se obtienen en total? \n\t\t(c)¿Cuál es el descuento total? \n\t\t(d)¿Cuál es el precio final de todos los libros? \n\t\t(e)¿Cuál es precio final de un libro?",
        "w es DESCUENTO POR CADA 10 LIBROS",
    ),
    (
        "En un colegio hay 180 estudiantes en quinto de primaria. Se necesita comprar un ejemplar de un libro de lectura para cada estudiante. Cada ejemplar cuesta 25 euros pero nos hacen un descuento de 20 euros por cada 10 ejemplares que compramos. ¿Cuánto dinero tendrá que pagar cada estudiante?",
        "y es PRECIO INICIAL DE UN LIBRO",
    ),
    (
        "Este curso la equipación de educación física cuesta 4€ menos que el curso pasado. Por 24 equipaciones se ha pagado 1344€ este año. ¿Cuánto dinero costaba una equipación el curso pasado?",
        "x es NÚMERO DE EQUIPACIONES, v es PRECIO DE MENOS DE UNA EQUIPACIÓN ESTE CURSO",
    ),
    (
        "Para un torneo de fútbol juvenil, se ha trasladado a los equipos usando 32 autobuses con 26 plazas cada uno. Si los desplazados se van a ubicar en hoteles de 208 plazas. ¿Cuántos hoteles harán falta?",
        "c es NÚMERO DE PERSONAS POR HOTEL",
    ),
    (
        "Para ir a un festival escolar de teatro, los colegios de una localidad han llenado 16 autobuses grandes con 40 plazas cada uno y 56 autobuses pequeños con 24 plazas cada uno. Si en cada fila del teatro donde se harán las representaciones caben 8 personas.¿Cuántas filas se ocuparán en total?",
        "u es NÚMERO DE PERSONAS EN CADA AUTOBÚS GRANDE, v es NÚMERO DE AUTOBUSES GRANDES, x es NÚMERO DE PERSONAS QUE CABEN EN UNA FILA, y es NÚMERO DE AUTOBUSES PEQUEÑOS, c es NÚMERO DE PERSONAS EN CADA AUTOBÚS PEQUEÑO",
    ),
    (
        "Me he apuntado a un club de atletismo para mejorar mi forma física. El club ofrece dos procedimientos de pago. Se puede optar por pagar 24 euros al principio de cada mes o 264 euros al principio del año. Como no sabía si me iba a gustar, opté por elegir el plan mensual. Después de 3 años decidí cambiar a la opción anual. ¿Cuánto dinero hubiera ahorrado si hubiera elegido la opción anual desde el principio?",
        "",
    ),
    (
        "Un vendedor de fruta y verdura compra mangos a 64€ el contenedor y los vende a 8€ el kilo. Sabiendo que un contenedor contiene 32 kilos. ¿Cuántos contenedores ha de vender para ganar 1344€?",
        "x es BENEFICIO TOTAL, a es PRECIO DE COMPRA DE UN CONTENEDOR, c es KILOS DE MANGOS EN UN CONTENEDOR",
    ),
    (
        "Una fábrica de juguetes debe producir 850 juegos de mesa en tres días. El primer día produce 112 y el segundo 3 veces más que el primero. ¿Cuántos juegos deberá producir el tercer día?",
        "",
    ),
    (
        "El pasado fin de semana hubo un concierto de música y la entrada individual costaba 24€. Ramón quiso invitar a 5 amigos al concierto  para celebrar su cumpleaños. Si tras pagar todas las entradas le sobraron 8 euros. ¿Cuánto dinero llevó al concierto?",
        "u es NÚMERO DE PERSONAS QUE INVITAN",
    ),
    (
        "María tiene 39 bolígrafos rojos, 41 azules y 19 negros. Los bolígrafos rojos vienen en packs de 3 bolígrafos y los azules y negros en packs de 2 bolígrafos.Si Paco tiene 87 bolígrafos entre bolígrafos azules y negros en total.¿Cuántos packs de bolígrafos rojos debe comprar para tener los mismos bolígrafos que María?",
        "w es NÚMERO DE BOLÍGRAFOS AZULES Y NEGROS DE PACO, a es NÚMERO DE BOLÍGRAFOS NEGROS EN CADA PACK, u es NÚMERO DE BOLÍGRAFOS AZULES DE MARÍA, b es NÚMERO DE BOLÍGRAFOS ROJOS DE MARÍA, y es NÚMERO DE BOLÍGRAFOS ROJOS EN CADA PACK, c es NÚMERO DE BOLÍGRAFOS AZULES EN CADA PACK, v es NÚMERO DE BOLÍGRAFOS NEGROS DE MARÍA",
    ),
    (
        "Suelo realizar atletismo 3 veces a la semana.Si habitualmente mi sesión de entrenamiento es de 180 minutos. \n\t ¿Cuántas horas practico atletismo a la semana?",
        "x es NÚMERO DE SESIONES, v es NÚMERO DE MINUTOS EN UNA HORA, c es DURACIÓN DE UNA SESIÓN EN MINUTOS",
    ),
    (
        "Una tienda de ropa quiere presentar las novedades de una conocida marca. Para ello, dispone de 8 maniquíes. Si la marca les ha mandado camisetas de 6 tipos diferentes y pantalones de 4 tipos diferentes. ¿Cuántos maniquíes necesitará conseguir la tienda para poder enseñar todas las combinaciones de ropa posibles?",
        "",
    ),
    (
        "Las clases de quinto y sexto de Primaria están vendiendo galletas a la salida del colegio para poder costear el viaje de fin de curso. Cada fin de semana preparan 400 galletas entre ambos cursos para poder venderlas. Para esta semana aún quedan la quinta parte de las galletas producidas la semana anterior. Sabiendo que a la clase de sexto de Primaria esta semana producirá 130 galletas. ¿Cuántas galletas debe preparar la clase de quinto?",
        "w es NÚMERO DE GALLETAS PRODUCIDAS CADA SEMANA",
    ),
    (
        "José está preparando un mural de fotos en una cartulina en la que caben 15 filas de fotos. Sabiendo que lleva colocadas 3 filas de fotos y que hay 39 fotos en estas filas. ¿Cuántas fotos le quedan por colocar?",
        "z es NÚMERO DE FOTOS COLOCADAS, y es NÚMERO DE FILAS COMPLETADAS",
    ),
    (
        "Se han inscrito 441 estudiantes en actividades deportivas esta temporada. En baloncesto hay 27 estudiantes más que en patinaje y en natación hay 4 veces más estudiantes que en baloncesto. ¿Cuántos estudiantes hay incritos en patinaje?",
        "u es NÚMERO DE ESTUDIANTES QUE HAY DE MÁS EN BALONCESTO QUE EN PATINAJE, z es NÚMERO DE ESTUDIANTES, x es NÚMERO DE VECES QUE HAY MÁS ESTUDIANTES EN NATACIÓN QUE EN BALONCESTO",
    ),
]
