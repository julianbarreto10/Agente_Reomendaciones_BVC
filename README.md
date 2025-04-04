
# Agente Autónomo de Inteligencia Artificial para Decisiones de Inversión en la Bolsa de Valores de Colombia

Este repositorio contiene el código y los recursos desarrollados para la implementación y evaluación de un agente autónomo basado en inteligencia artificial, orientado a generar recomendaciones automáticas de inversión en los principales títulos de renta variable de la Bolsa de Valores de Colombia.

## Estructura del Repositorio

- **`Agent_utils`**: Incluye herramientas de utilidad para el agente autónomo, especialmente documentos empleados por el agente con técnicas de Retrieval-Augmented Generation (RAG).

- **`Estrategias_tradicionales`**: Implementación de estrategias clásicas de inversión:
  - Media Móvil
  - Reversión a la Media
  - Comprar y Mantener

- **`Prompts`**: Contiene los templates de prompts empleados por el agente autónomo para interactuar con el gran modelo de lenguaje (LLM).

- **`Resultados_Experimento`**: Almacena los resultados obtenidos tras la evaluación del agente y las estrategias tradicionales para los títulos bursátiles analizados:
  - Bancolombia (`PFBCOLOM.CL`)
  - Ecopetrol (`ECOPETROL.CL`)
  - Nutresa (`NUTRESA.CL`)
  - Cementos Argos (`CEMARGOS.CL`)

- **`Scrapings`**: Código para la recopilación automática de datos relevantes mediante web scraping desde diversas fuentes, incluyendo:
  - Informes financieros (BVC)
  - Noticias económicas
  - Análisis de mercado
  - Información del Banco de la República
  - Datos históricos de acciones

- **`agent.py`, `agent_history_experiment.py`, `agent_run.py`**: Scripts principales para ejecutar el agente autónomo, realizar experimentos históricos y pruebas en tiempo real.

- **`evaluation_metrics.py`**: Código para evaluar el desempeño del agente mediante métricas financieras estándar.

- **`analisis_resultados.ipynb`**: Notebook de análisis y visualización de resultados obtenidos en los experimentos.

## Instalación

Para instalar las dependencias necesarias, ejecutar:

```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar el agente autónomo en tiempo real:

```bash
python agent_run.py
```

Para realizar experimentos históricos:

```bash
python agent_history_experiment.py
```