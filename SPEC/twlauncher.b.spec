%global beta 1

Name:           twlauncher.b
Version:        1.2.2
Release:        2%{?dist}
Summary:        Launcher for most popular Teeworlds clients.
License:        Unknown
URL:            https://twlauncher.netlify.app/
Source0:        https://github.com/noxygalaxy/TWLauncher/releases/download/v%{version}-beta.%{beta}/TWLauncher-x86_64.AppImage
Source1:        https://rxelelo.gitlab.io/rxrepo/rxrepo/os/x86_64/twlauncher.png
ExclusiveArch:  x86_64

# Runtime dependencies
Requires:       freetype       
Requires:       libnotify
Requires:       curl
Requires:       sqlite
Requires:       fuse 
Requires:       gtk3
Requires:       nss
Requires:       alsa-lib
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       libXi

# Build dependencies
BuildRequires:  tar
BuildRequires: patchelf

#Conflicts
Conflicts: twlauncher
%description
A DDRaceNetwork modification adding new features. DDRaceNetwork is a 
multiplayer racing game based on Teeworlds with additional gameplay 
mechanics and features.

%global debug_package %{nil}
%prep
%setup -c -T


%build

%install
install -dm0755 %{buildroot}/opt
install -dm0755 %{buildroot}%{_bindir}
install -dm0755 %{buildroot}%{_datadir}/applications
install -dm0755 %{buildroot}/opt/%{name}
install -dm0755 %{buildroot}/opt/%{name}/game

cp -a %{SOURCE0} %{buildroot}/opt/%{name}/

chmod +x %{buildroot}/opt/%{name}/TWLauncher-x86_64.AppImage

cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
exec /opt/twlauncher-bin/TWLauncher-x86_64.AppImage
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Version=$pkgver
Name=TWLauncher
StartupNotify=true
TryExec=twlauncher
Exec=twlauncher
Terminal=false
Icon=/opt/twlauncher/twlauncher.png
Type=Application
Categories=Game
EOF

install -Dm644 %{SOURCE1} %{buildroot}/opt/%{name}/%{name}.png

for binary in %{buildroot}/opt/%{name}/*; do
    if file "$binary" | grep -q "ELF.*executable"; then
        patchelf --set-rpath '$ORIGIN' "$binary" 2>/dev/null || true
    fi
done


%files
/opt/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Aug 10 2025 Rain Xelelo <rxelelo@outlook.com> - 1.14-2
- Initial package for Fedora