%define	Summary	An enhanced version of DooM - classic 3D shoot-em-up game

Summary:	%{Summary}
Name:		prboom
Version:	2.5.0
Release:	8
Source0:	http://prdownloads.sourceforge.net/prboom/%{name}-%{version}.tar.bz2
Source1:	%{name}-game-server.sysconfig
Source2:	%{name}-game-server.service
Source3:	doom2-newcaco16.png
Source4:	doom2-newcaco32.png
Source5:	doom2-newcaco48.png
Source6:	%{name}-game-server.wrapper
URL:		http://prboom.sourceforge.net/
Group:		Games/Arcade
License:	GPL
BuildRequires:	smpeg-devel
BuildRequires:	sed
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_net)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(SDL_mixer)
Requires:	TiMidity++
Requires:	doom-iwad

%description
Doom is the classic 3D shoot-em-up game. It must have been one of the best
selling games ever; it totally outclassed any 3D world games that preceded
it, with amazing speed, flexibility, and outstanding gameplay. The specs
to the game were released, and thousands of extra levels were written by
fans of the game; even today new levels are written for Doom faster then
any one person could play them.

-- NOTE : YOU NEED TO DOWNLOAD WAD FILES --
http://www.idsoftware.com/

%package gl
Summary:	OpenGL version
Group:		Games/Arcade
Requires:	%{name}

%description gl
This package contains the PrBooM binary that runs accelerated through
OpenGL.

%package server
Summary:	PrBooM game server
Group:		Games/Arcade
Requires(pre):	rpm-helper
Requires:	%{name}

%description server
This package contains the PrBooM server binary, that is the program 
that passes data between the different players in the game.

%prep
%setup -q

%build
%define common_conf_flags --disable-cpu-opt --disable-i386-asm
%configure %{common_conf_flags} --enable-gl
%make
cp src/prboom prboom-gl

make clean

%configure %{common_conf_flags} --disable-cpu-opt
%make

%install
%makeinstall_std
install -m755 prboom-gl %{buildroot}%{_gamesbindir}

# delete unwanted files
rm -fr %{buildroot}%{_datadir}/doc/

#
# Initscript
install -d %{buildroot}%{_sysconfdir}/sysconfig \
	   %{buildroot}%{_unitdir}

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-game-server
cp %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-game-server.service

sed -i "s|/etc/sysconfig|%{_sysconfdir}/sysconfig| ; s|/usr/games|%{_gamesbindir}|" \
%{buildroot}%{_unitdir}/%{name}-game-server.service

#
# Icons
install -m644 %{SOURCE3} -D %{buildroot}%{_miconsdir}/doom2-newcaco.png
install -m644 %{SOURCE4} -D %{buildroot}%{_iconsdir}/doom2-newcaco.png
install -m644 %{SOURCE5} -D %{buildroot}%{_liconsdir}/doom2-newcaco.png

#
# Wrapper to launch server
install -m755 %{SOURCE6} -D %{buildroot}%{_gamesbindir}/%{name}-game-server.wrapper

#
# Menus

mkdir -p %{buildroot}%{_datadir}/applications/

cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=PrBooM
Comment=%{Summary}
Icon=doom2-newcaco
Exec=%{_gamesbindir}/%{name}
EOF

cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}-multiplayer.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=PrBooM Multiplayer
Comment=%{Summary}
Icon=doom2-newcaco
Exec=sh -c "%{_gamesbindir}/%{name} -net \`hostname\`"
EOF

cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}-gl.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=PrBooM-GL
Comment=%{Summary}
Icon=doom2-newcaco
Exec=%{_gamesbindir}/%{name}-gl
EOF

cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}-gl-multiplayer.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=PrBooM-GL Multiplayer
Comment=%{Summary}
Icon=doom2-newcaco
Exec=sh -c "%{_gamesbindir}/%{name}-gl -net \`hostname\`"
EOF


%post server
%systemd_post %{name}-game-server.service

%preun server
%systemd_preun %{name}-game-server.service

%postun server
%systemd_postun_with_restart %{name}-game-server.service

%files
%doc AUTHORS NEWS README TODO
%doc doc/*.txt doc/README.*
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/doom
%{_gamesdatadir}/doom/%{name}.wad
%{_mandir}/man5/*
%{_mandir}/man6/%{name}.6*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-%{name}-multiplayer.desktop
%{_iconsdir}/doom2-newcaco.png
%{_miconsdir}/doom2-newcaco.png
%{_liconsdir}/doom2-newcaco.png

%files gl
%{_gamesbindir}/%{name}-gl
%{_datadir}/applications/mandriva-%{name}-gl.desktop
%{_datadir}/applications/mandriva-%{name}-gl-multiplayer.desktop

%files server
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-game-server
%{_unitdir}/%{name}-game-server*
%{_gamesbindir}/%{name}-game-server*
%{_mandir}/man6/%{name}-game-server*
