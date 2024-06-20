from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_pdf_path, output_folder):
    pdf_reader = PdfReader(input_pdf_path)
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output_pdf_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
        
        with open(output_pdf_path, 'wb') as out:
            pdf_writer.write(out)
            print(f'Page {page_num + 1} saved to {output_pdf_path}')

def main():
    input_path = input("Enter the path of the PDF file to split: ").strip()
    output_folder = input("Enter the output folder path: ").strip()
    
    split_pdf(input_path, output_folder)

if __name__ == "__main__":
    main()
