from django.shortcuts import render
from django.views import View
from App import models
import re
import json
import time
from googletrans import Translator


def traducir_texto(traductor,texto, codigo_idioma_destino):
    solve = False
    while solve==False:
        traduccion = traductor.translate(texto, dest=codigo_idioma_destino)
        solve = True
    return traduccion.text


def traducir_diccionario(diccionario, codigo_idioma_destino):
    traductor = Translator()
    def traducir_valores(diccionario):
        for clave, valor in diccionario.items():
            if isinstance(valor, dict):
                diccionario[clave] = traducir_valores(valor)
            elif isinstance(valor, str):
                diccionario[clave] = traducir_texto(traductor, valor, codigo_idioma_destino)
                print(f"{clave} ===>> {diccionario[clave]}")
        return diccionario
    return traducir_valores(diccionario.copy())




def diccionario_a_json_string(diccionario):
    """
    Convierte un diccionario de Python a una cadena JSON.
    
    :param diccionario: Diccionario de Python
    :return: Cadena JSON
    """
    json_string = json.dumps(diccionario)
    return json_string


def json_string_a_diccionario(json_string):
    """
    Convierte una cadena JSON a un diccionario de Python.
    
    :param json_string: Cadena JSON
    :return: Diccionario de Python
    """
    diccionario = json.loads(json_string)
    return diccionario






class Index(View):
    def get(self, request):
        contenido = {
            'navbar':{
                'home':"Start",
                'services':"Services",
                'team':"Our Team",
                'contact':"Contact"
            },
            'header':{
                'seccion1':{
                            'etiqueta':"Business Solution",
                            'span':"We Deliver Results",
                            'h1':"Strategy Development & Technical Support",
                            'p':"We help develop and execute marketing strategies, including content marketing, SEM, and SMM. Additionally, we offer web development, process automation, and technical support to ensure your operations run smoothly and efficiently."
                        },
                'seccion2':{
                            'etiqueta':"Business Solution",
                            'span':"Consulting Services",
                            'h1':"Content Creation & Customer Support",
                            'p':"Our team designs and writes attractive, relevant posts for your audience on Twitter, Facebook, and Instagram. We also provide customer support by responding to inquiries and resolving user issues on social media."
                        },
                'seccion3':{
                            'etiqueta':"Business Solution",
                            'span':"We Provide Quality",
                            'h1':"Social Media Management",
                            'p':"We offer comprehensive social media management for Twitter, Facebook, and Instagram. This includes profile creation, promotional design, and result analysis. Our services ensure your social media presence is engaging and effective."
                        },
                'boton':'Discover More'
            },
            'services':{
                'header':{
                        'etiqueta':"What We Offer You",
                        'h1':"Our Services",
                        'p':"We use the latest technologies like Django, Bootstrap 5, and AWS EC2 to bring your ideas to life. Let’s make something amazing together!"
                    },
                'servicios':{
                    "s1":{
                            "titulo":"Website Implementation",
                            "p1":"Need a Stunning Website? Let’s Go! Get a custom-designed, fully functional website for your business.",
                            "description":"Description:",
                            "p2":"Creation of a website that showcases company information. This service includes:",
                            "li1":"Custom website design.",
                            "li2":"Site development and programming.",
                            "li3":"Initial setup and configuration.",
                            "li4":"DNS configuration.",
                            "li5":"SSL certificate issued by a certifying authority.",
                            "li6":"Search Engine Optimization (SEO)",
                            "span":"Approximate Price:",
                            "precio":"Between 250 and 300 USD, depending on the complexity and features of the site."
                        },
                    "s2":{
                            "titulo":"Business Process Automation",
                            "p1":"Automate Your Business Processes! Streamline your operations with automated solutions, from inventory management to complex workflows.",
                            "description":"Description:",
                            "p2":"Implementation of automated solutions for one or more business processes. This service includes:",
                            "li1":"Inventory management.",
                            "li2":"Report generation.",
                            "li3":"Automation of simple tasks.",
                            "li4":"Optimization of complex workflows.",
                            "li5":"DNS configuration.",
                            "li6":"SSL certificate issued by a certifying authority.",
                            "li7":"Search Engine Optimization (SEO)",
                            "span":"Approximate Price:",
                            "precio":"Between 600 and 3,000 USD, depending on the scope and complexity of the processes to be automated."
                        },
                    "s3":{
                            "titulo":"Strategy Development",
                            "p1":"Strategic Marketing Solutions! Elevate your brand with tailored marketing strategies",
                            "description":"Description:",
                            "p2":"Assistance in creating and executing marketing strategies on social media. This service includes:",
                            "li1":"Content marketing.",
                            "li2":"Search Engine Marketing (SEM).",
                            "li3":"Social Media Marketing (SMM).",
                            "span":"Price:",
                            "precio":"300 USD per month."
                        },
                    "s4":{
                            "titulo":"Monthly Web Server Hosting",
                            "p1":"Reliable Web Hosting on AWS! Host your website on powerful AWS EC2 instances, tailored to your needs. Enjoy seamless performance and expert support.",
                            "description":"Description:",
                            "p2":"Hosting the web server that supports the company's website, using EC2 instances on AWS. This service includes:",
                            "li1":"Configuration and management of servers on AWS.",
                            "li2":"Selection of appropriate EC2 instances based on the needs of the implemented platform.",
                            "li3":"Server monitoring and maintenance.",
                            "li4":"Technical support for the server.",
                            "span":"Approximate Price:",
                            "precio":"Between 70 and 2,300 USD per month, depending on site consumption, storage load, and server characteristics."
                        },
                    "s5":{
                            "titulo":"Social Media Management",
                            "p1":"Boost Your Social Media Presence! Let us manage your social media profiles with daily posts, promotions, and engagement. Get detailed analytics and custom designs",
                            "description":"Description:",
                            "p2":"Comprehensive management of the company's social media profiles. This service includes:",
                            "li1":"Management of profiles on Twitter, Facebook, and Instagram.",
                            "li2":"Creation of social profiles (if not already existing).",
                            "li3":"Design of promotions, offers, and services tailored to the niche.",
                            "li4":"Results analysis with monthly reports.",
                            "li5":"Comment moderation and response to inquiries.",
                            "li6":"Custom design of social media covers and backgrounds.",
                            "li7":"3 tweets per day on Twitter.",
                            "li8":"3 posts per day on Facebook.",
                            "li9":"3 posts per day on Instagram",
                            "span":"Price:",
                            "precio":"400 USD per month."
                        },
                    "s6":{
                            "titulo":"Social Media Content Creation",
                            "p1":"Engaging Content Creation! Captivate your audience with professionally designed and written social media posts. Perfect for Twitter, Facebook, and Instagram.",
                            "description":"Description:",
                            "p2":"Transform your social media with irresistible and high-impact content. Our service includes:",
                            "li1":"Customized Posts: We design and write exclusive content for Twitter, Facebook, and Instagram, tailored to your brand and audience.",
                            "li2":"Persuasive Texts: We create messages that capture attention and generate engagement.",
                            "li3":"Impactful Visual Design: We develop images and graphics that stand out in the feed and attract your audience.",
                            "li4":"Trend Adaptation: We stay up-to-date with the latest trends to ensure your content is always at the forefront.",
                            "span":"Price:",
                            "precio":"200 USD per month."
                        },
                    "s7":{
                            "titulo":"Customer Support",
                            "p1":"Responsive Customer Support! Ensure your customers get the help they need with our dedicated social media support service. Fast, friendly, and efficient.",
                            "description":"Description:",
                            "p2":"Enhance your customer experience with our responsive and efficient social media support. Our service includes:",
                            "li1":"Real-Time Inquiry Management: Promptly address and resolve user inquiries and issues on social media platforms.",
                            "li2":"Personalized Responses: Craft tailored responses to ensure customer satisfaction and loyalty.",
                            "li3":"Proactive Engagement: Monitor and engage with your audience to preemptively address potential concerns.",
                            "span":"Price:",
                            "precio":"180 USD per month."
                        },
                    "s8":{
                            "titulo":"Technical Support",
                            "p1":"Optimize your website and server with our premium technical support! No more worries about maintenance and updates.",
                            "description":"Description:",
                            "p2":"Technical support service for contracted websites and servers. This service includes:",
                            "li1":"Routine maintenance.",
                            "li2":"Minor and major updates.",
                            "li3":"Problem resolution.",
                            "span":"Approximate Price:",
                            "hp1":"Basic Support:",
                            "precio1":"Between 30 and 50 USD per month per user. Includes routine maintenance, minor updates, and resolution of basic issues.",
                            "hp2":"Intermediate Support:",
                            "precio2":"Between 50 and 100 USD per month per user. Includes more complex updates, preventive maintenance, and resolution of moderate issues.",
                            "hp3":"Advanced Support:",
                            "precio3":"Between 100 and 200 USD per month per user. Includes major updates, significant infrastructure changes, proactive maintenance, and resolution of complex issues."
                        },
                },
            },
            'team':{
                'header':{
                    'span':"Our Team",
                    'h2':"Our Creative Team",
                    'p':"Our team of experts is dedicated to providing high-quality services, specifically designed for small and medium-sized businesses. We take pride in our innovative solutions and personalized approach, ensuring that your business thrives in the digital environment.",
                },
                'elias':{
                    'nombre':"Elías Eduardo Liranza Pérez",
                    'cargo':"Founder - CEO",
                    'p':"Cybersecurity Engineer, Fullstack Developer, and Entrepreneur."
                },
                'melanie':{
                    'nombre':"Melanie Tamayo Casademut",
                    'cargo':"Founder - Director of Digital Marketing",
                    'p':"Bachelor in Tourism, Community Manager, Specialist in Digital Marketing, Content Creator, Entrepreneur"
                }
            },
            'contacto':{
                'header':{
                    'span':"Get to Know Us",
                    'h2':'We Are Very Good In Boosting Your Businesses',
                    'p':'Boost your business with our web development, process automation, and digital marketing services, designed to maximize your growth and efficiency!',
                },
            }
        }
        # Obtener la cabecera 'Accept-Language'
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        # Extraer el primer idioma de la lista
        user_language = accept_language.split(',')[0] if accept_language else 'en'
        user_language = re.split(r'[^a-zA-Z]', user_language, 1)[0]
        
        if user_language == 'en':
            return render(request,"index.html",{
                "contenido":contenido
            })
        else:
            if models.ContenidoTraducido.objects.filter(idioma=user_language).exists():
                traducido = models.ContenidoTraducido.objects.get(idioma=user_language).contenido
                traducido = json_string_a_diccionario(traducido)
                return render(request,"index.html",{
                    "contenido":traducido
                })
            else:
                traducido = traducir_diccionario(diccionario=contenido,codigo_idioma_destino=user_language)
                dbtr = models.ContenidoTraducido(idioma=user_language,contenido=diccionario_a_json_string(traducido))
                dbtr.save()
                return render(request,"index.html",{
                    "contenido":traducido
                })
