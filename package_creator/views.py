import subprocess
from django.shortcuts import render
from .forms import PackageForm

def create_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            passphrase = form.cleaned_data['passphrase']
            password = form.cleaned_data['password']

            if password != form.cleaned_data['confirm_password']:
                return render(request, 'create_package.html', {'form': form, 'error': 'Passwords do not match!'})

            try:
                # Generate SSH keys and capture logs
                key_path = f"/home/pmorey/keys/{username}_id_rsa"
                ssh_keygen_command = [
                    'ssh-keygen', '-t', 'rsa', '-C', f"{username}@promptcloud.com",
                    '-f', key_path, '-N', passphrase
                ]
                ssh_keygen_result = subprocess.run(
                    ssh_keygen_command,
                    capture_output=True,
                    text=True
                )

                # Create Debian package and capture logs
                package_command = [
                    '/home/pmorey/bin_pmorey/ruby.sh',
                    '/home/pmorey/bin_pmorey/sys/setup/infra/debian_packages/user_administration/create_promptcloud_user/create_package.rb',
                    '-u', username,
                    '-f', f"{key_path}.pub"
                ]
                package_result = subprocess.run(
                    package_command,
                    input=f"{password}\n{password}\n",
                    capture_output=True,
                    text=True
                )

                # Combine logs for display
                logs = (
                    f"SSH Key Generation Output:\n{ssh_keygen_result.stdout}\n{ssh_keygen_result.stderr}\n\n"
                    f"Debian Package Creation Output:\n{package_result.stdout}\n{package_result.stderr}"
                )

                return render(request, 'create_package.html', {
                    'form': form,
                    'success': 'Package created successfully!',
                    'logs': logs
                })

            except Exception as e:
                return render(request, 'create_package.html', {
                    'form': form,
                    'error': f"An error occurred: {str(e)}"
                })
    else:
        form = PackageForm()

    return render(request, 'create_package.html', {'form': form})
