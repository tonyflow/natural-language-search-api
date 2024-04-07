FROM python as search_api_base_image

WORKDIR /usr/niko/natural-language-search-api

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Place your hugging face API token here
ENV BEARER_TOKEN=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

COPY . .
EXPOSE 8000

CMD ["uvicorn", "router:natural_language_search", "--reload", "--host", "0.0.0.0", "--port", "8000"]
