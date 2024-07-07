import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


LlamaParse_api_key = "llx-rGnYIa6alLxmW2PnOI0baqEwQV37QAkfiG87VK2fkJnCZCcd"

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def llama_parser(api_key):
    parser = LlamaParse(
        api_key=api_key,
        result_typt="markdown"
    )
    return parser

def directory_reader(parser):
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files= , file_extractor=).load_data() #read more about this object 



'''TODO - MAKE A LIST OF ALREADY PARSED FILES AS FILES WILL BE PASSED INDIVIDUALLY '''


class PDFHandler(FileSystemEventHandler):
    #use a monitor with watchdog if the new added file is a pdf file then call the proces pdf function
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            self.process_pdf(event.src_path)

    #the process pdf function will call llammaparde and parse the new found file
    def process_pdf(self, pdf_path):
        print(f"Procesando: {pdf_path}")
        '''CAUTION THIS FUNCTION MAY NOT WORK WITH LLAMAPARSE AS IT IS NOT USING CORRECTLY LLAMAPARSE'''
        parser = LlamaParse()
        try:
            parsed_data = parser.parse(pdf_path)
            output_path = os.path.join(OUTPUT_DIR, os.path.basename(pdf_path) + ".txt")
            with open(output_path, "w") as f:
                f.write(f"Título: {parsed_data.title}\n")
                f.write(f"Autor: {parsed_data.author}\n")
                f.write(f"Fecha: {parsed_data.date}\n")
                f.write(f"Texto:\n{parsed_data.text}")
            print(f"Procesamiento completado: {output_path}")
        except Exception as e:
            print(f"Error al procesar {pdf_path}: {str(e)}")

if __name__ == "__main__":
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIR, recursive=False)
    observer.start()

    #this prigram will kep an oobsrver alive in the datalake 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()