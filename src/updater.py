import requests
import os
import zipfile
from json import dump, load
from packaging.version import Version
import urllib3
from ttkbootstrap.dialogs.dialogs import Messagebox
import ttkbootstrap as ttk
import shutil

zip_file = '.\\Python-Macro.zip'

# Get rid of annoying 'insecure request' error
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


def new_version_available(owner, repo, settings):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = requests.get(url, verify=False)
    response.raise_for_status()
    data = response.json()

    return Version(data['tag_name'].replace('v', '')) > Version(settings['version'])


def download_latest_release(owner, repo, save_path='.'):
    # Ensure the dir exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Get the latest release info
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = requests.get(url, verify=False)
    response.raise_for_status()

    release_data = response.json()
    # Print release info
    print(f"Latest release: {release_data['name']}")
    print(f"Published at: {release_data['published_at']}")
    print(f"Tag: {release_data['tag_name']}")
    print(f"URL: {release_data['html_url']}")

    # Download the assets
    for asset in release_data['assets']:
        asset_url = asset['browser_download_url']
        asset_name = asset['name']
        print(f"Downloading {asset_name} from {asset_url}")

        asset_response = requests.get(asset_url, stream=True, verify=False)
        asset_response.raise_for_status()

        file_path = os.path.join(save_path, asset_name)
        with open(file_path, 'wb') as file:
            for chunk in asset_response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded {asset_name} to {file_path}")


def extract_specific_directory(zip_path, target_dir, extract_to):

    extracted = False

    if not target_dir.endswith('/'):
        target_dir += '/'  # Ensure target_dir ends with a slash

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            # Check if the file is within the target directory
            if member.filename.startswith(target_dir):
                # Create a new name for the file to be extracted
                # by stripping off the target directory path
                relative_path = os.path.relpath(member.filename, target_dir)
                extract_path = os.path.join(extract_to, relative_path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(extract_path), exist_ok=True)

                # Extract the file
                if not member.is_dir():
                    print(f'Extracting {member.filename} to {extract_path}')
                    extracted = True
                    with zip_ref.open(member) as source, open(extract_path, 'wb') as target:
                        target.write(source.read())

        if not extracted:
            raise Exception(f'Could not extract {target_dir} to {extract_to}')


def extract_specific_file(zip_path, file_name, extract_to):

    extracted = False

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            if member.filename == file_name:
                # Ensure the dir exists
                os.makedirs(os.path.dirname(extract_to), exist_ok=True)

                # Extract the file
                print(f'Extracting {member.filename} to {extract_to}')
                with zip_ref.open(member) as source, open(extract_to, 'wb') as target:
                    target.write(source.read())

                extracted = True

                break
        if not extracted:
            raise Exception(f'Could not extract {file_name} to {extract_to}')

if __name__ == "__main__":

    # Ensure working dir is macro root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')

    owner = 'Jaxx7594'
    repo = 'Python-Macro'
    save_path = './main.dist'

    # Make a backup of the users settings so they can be reapplied after settings file replacement
    with open('settings.json', 'r') as file:
        settings_backup = load(file)

    if not new_version_available(owner, repo, settings_backup):
        print('Current installation is already latest version. Exiting.')

        root = ttk.Window()
        root.style.theme_use('darkly')
        result = Messagebox.show_error(title='Already latest version', message='The current installation is already the latest version. The updater is now exiting.')
        root.destroy()

        exit()

    root = ttk.Window()
    root.style.theme_use('darkly')
    result = Messagebox.show_info(title='Updater', message="Welcome to the updater. Press 'Ok' to continue. We'll let you know when we're finished.")
    root.destroy()
    
    if not os.path.exists('./Python-Macro.zip'):
        # Download the latest release and get the path of the downloaded file
        download_latest_release(owner, repo)

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    # Extract required files and images
    extract_specific_directory(zip_file, 'Macro/main.dist', './main.dist')
    extract_specific_directory(zip_file, 'Macro/images', './images')

    # Extract settings file (for if any new entries are added)
    extract_specific_file(zip_file, 'Macro/settings.json', './settings.json')

    # Delete zip after extraction
    os.remove(zip_file)
    print(f"Deleted zip file {zip_file}")

    # Reapply settings
    with open('settings.json', 'r+') as file:
        settings = load(file)
        settings['first_time_running'] = settings_backup['first_time_running']
        settings['selected_profile'] = settings_backup['selected_profile']
        settings['profiles'] = settings_backup['profiles']

        file.seek(0)
        file.truncate()
        dump(settings, file, indent=4)

    root = ttk.Window()
    root.style.theme_use('darkly')
    result = Messagebox.show_info(title='Update complete', message="The update has finished. You can now restart the macro.")
    root.destroy()
