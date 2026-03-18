%global _name CatClient

Name:           catclient
Version:        1.0.2
Release:        1%{?dist}
Summary:        Yet another fork of TaterClient for DDNet
License:        Unknown
URL:            https://github.com/quomy/CatClient/
Source0:        https://github.com/quomy/CatClient/releases/download/%{version}/CatClient-%{version}-linux_x86_64.tar.gz
Source1:        https://rxelelo.gitlab.io/rxrepo/icons/%{name}.png
ExclusiveArch:  x86_64

# Runtime dependencies
Requires:       (freetype or libfreetype6)
Requires:       opusfile
Requires:       curl
Requires:       glew
Requires:       wavpack
Requires:       (ffmpeg-free or ffmpeg or libavcodec-free)
Requires:       libnotify
Requires:       miniupnpc
Requires:       sqlite
Requires:       mariadb-connector-c
Requires:       vulkan-loader

# Build dependencies
BuildRequires:  tar
BuildRequires: patchelf

%description
A DDRaceNetwork modification adding new features. DDRaceNetwork is a 
multiplayer racing game based on Teeworlds with additional gameplay 
mechanics and features.

%global debug_package %{nil}
%prep
%setup -c -T
mkdir -p %{name}
tar xf %{SOURCE0} -C %{name}

%build

%install
install -dm0755 %{buildroot}/opt
install -dm0755 %{buildroot}%{_bindir}
install -dm0755 %{buildroot}%{_datadir}/applications
install -dm0755 %{buildroot}/opt/%{name}
install -dm0755 %{buildroot}/opt/%{name}/game

cp -a %{name}/%{_name}-*-linux_x86_64/* %{buildroot}/opt/%{name}/game

chmod +x %{buildroot}/opt/%{name}/game/%{_name}

cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
cd /opt/%{name}/game/
exec ./%{_name} "$@"
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=%{_name}
Comment=A DDRaceNetwork modification adding new features
Exec=%{name}
Icon=/opt/%{name}/%{name}.png
Terminal=false
Type=Application
Categories=Game;
EOF

install -Dm644 %{SOURCE1} %{buildroot}/opt/%{name}/%{name}.png

for binary in %{buildroot}/opt/%{name}/game/*; do
    if file "$binary" | grep -q "ELF.*executable"; then
        patchelf --set-rpath '$ORIGIN' "$binary" 2>/dev/null || true
    fi
done


%files
/opt/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Mar 17 2026 Rain Xelelo <rxelelo@outlook.com> - 1.0.2-1
- Bump 1.0.2
* Tue Mar 17 2026 Rain Xelelo <rxelelo@outlook.com> - 1.0.1-1
- Inital 1.0.1
