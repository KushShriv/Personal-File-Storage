import os
import sys

# Define chunk size (25 MB in bytes)
CHUNK_SIZE = 25 * 1024 * 1024

def chunk_binary_pdf(file_name):
    """Chunks the PDF into binary parts, each under 25 MB."""
    try:
        folder_name = os.path.splitext(file_name)[0]  # Use the file name for folder name
        
        # Create folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        with open(file_name, 'rb') as pdf_file:
            chunk_num = 1
            while True:
                chunk_data = pdf_file.read(CHUNK_SIZE)
                if not chunk_data:
                    break
                chunk_file_name = os.path.join(folder_name, f'chunk_{chunk_num}')
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                chunk_num += 1

        print(f'PDF chunked into {chunk_num - 1} parts in folder: {folder_name}')
    
    except Exception as e:
        print(f'Error chunking PDF: {str(e)}')

def join_binary_chunks(folder_name):
    """Joins the binary chunks back into a single PDF."""
    try:
        chunk_files = sorted([os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.startswith('chunk_')])

        output_file = f'{folder_name}.pdf'
        with open(output_file, 'wb') as output_pdf:
            for chunk_file in chunk_files:
                with open(chunk_file, 'rb') as chunk:
                    output_pdf.write(chunk.read())

        print(f'Chunks joined into: {output_file}')

    except Exception as e:
        print(f'Error joining chunks: {str(e)}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <pdf_file_name> <chunk/join>")
        sys.exit(1)

    file_name = sys.argv[1]
    operation = sys.argv[2].lower()

    if operation == 'chunk':
        chunk_binary_pdf(file_name)
    elif operation == 'join':
        folder_name = os.path.splitext(file_name)[0]
        join_binary_chunks(folder_name)
    else:
        print("Invalid operation. Use 'chunk' or 'join'.")
