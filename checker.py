import requests
import re

def load_installed_packages(filename="software_report.txt"):
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def fetch_vulnerabilities(package, version):
    api_url = f"https://services.nvd.nist.gov/rest/json/cve/1.0"
    query_params = {
        "cpeMatchString": f"cpe:2.3:a:{package}:{package}:{version}:*:*:*:*:*:*:*",
        "addOns": "cves",
    }

    response = requests.get(api_url, params=query_params)

    if response.ok:
        return response.json().get("result", {}).get("CVE_Items", [])
    else:
        print(f"Failed to fetch vulnerabilities for {package} version {version}")
        return []

def check_vulnerabilities(installed_packages):
    vulnerable_packages = []
    for package_info in installed_packages:
        package, version = package_info.split(": ")
        vulnerabilities = fetch_vulnerabilities(package, version)
        if vulnerabilities:
            vulnerable_packages.append((package, version, vulnerabilities))

    return vulnerable_packages

def print_vulnerable_packages(vulnerable_packages):
    if not vulnerable_packages:
        print("No vulnerable packages found.")
    else:
        print("Vulnerable Packages:")
        for package, version, vulnerabilities in vulnerable_packages:
            print(f"Package: {package}, Version: {version}")
            for vulnerability in vulnerabilities:
                cve_id = vulnerability["cve"]["CVE_data_meta"]["ID"]
                print(f"  CVE ID: {cve_id}")
                description = vulnerability["cve"]["description"]["description_data"][0]["value"]
                print(f"  Description: {description}")
            print()

if __name__ == "__main__":
    try:
        installed_packages = load_installed_packages()
        vulnerable_packages = check_vulnerabilities(installed_packages)
        print_vulnerable_packages(vulnerable_packages)
    except FileNotFoundError:
        print("Error: The 'software_report.txt' file not found. Please generate it first.")
    except Exception as e:
        print(f"An error occurred: {e}")
