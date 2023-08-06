import subprocess
import pdfkit

def get_installed_packages():
    packages = {}
    
    output = subprocess.check_output('dpkg --get-selections | grep -v deinstall', shell=True)
    for line in output.decode().split('\n'):
        package = line.split()
        packages[package[1]] = package[0]
        
    return packages

def generate_pdf(packages):    
    html = ''
    for name, status in packages.items():
        html += f'<p><b>{name}</b> - {status}</p>'
        
    pdfkit.from_string(html, 'installed_software.pdf')

if __name__ == '__main__':
    packages = get_installed_packages()
    generate_pdf(packages)
