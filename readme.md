# Instrucciones


## 1 Instalar docker y compose

https://docs.docker.com/desktop/install/mac-install/
https://docs.docker.com/compose/install/

## 2 Clonar el repositorio

`git clone https://github.com/dbsiavichay/lender.git`

## 3 Levantar el proyecto

 - Renombrar el archivo `env.example` a `.env`
 - Construir con `docker-compose build`
 - Iniciar con `docker-compose up -d`
 - Correr migraciones con
	 - `make migrate` ó
	 - `docker-compose run --rm api python3 manage.py migrate`
 - Podremos hacer peticiones a `localhost:8000/api/`

## 4 Configuración adicional

 - Generar un api key con
	 - `make apikey` ó
	 - `docker-compose run -T --rm api python3 manage.py shell < ./scripts/apikey.py`
	 - Tendremos un output `Api-Key J3toPt8K.Ql4WDB0Cewdwr1jbRZz6GT09epTuawxG`

## 5 Documentación

La documentación la tendremos disponible en 
- `localhost:8000`