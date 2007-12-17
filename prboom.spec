%define version 2.4.7
%define name    prboom
%define release %mkrel 2
%define	Summary	An enhanced version of DooM - classic 3D shoot-em-up game

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/prboom/%{name}-%{version}.tar.bz2
Source1:	%{name}-game-server.sysconfig.bz2
Source2:	%{name}-game-server.init.bz2
Source3:	doom2-newcaco16.png
Source4:	doom2-newcaco32.png
Source5:	doom2-newcaco48.png
URL:		http://prboom.sourceforge.net/
Group:		Games/Arcade
License:	GPL
BuildRequires:	SDL-devel smpeg-devel SDL_mixer-devel SDL_net-devel
BuildRequires:	sed MesaGLU-devel
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

%configure --disable-cpu-opt --enable-gl
%make
cp src/prboom prboom-gl

make clean

%configure --disable-cpu-opt
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
install -m755 prboom-gl %{buildroot}%{_gamesbindir}

# delete unwanted files
rm -fr %{buildroot}%_datadir/doc/

#
# Initscript
install -d %{buildroot}%{_sysconfdir}/sysconfig \
	   %{buildroot}%{_initrddir}

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/sysconfig/%{name}-game-server
bzcat %{SOURCE2} > %{buildroot}%{_initrddir}/%{name}-game-server

sed -i "s|/etc/sysconfig|%{_sysconfdir}/sysconfig| ; s|/usr/games|%{_gamesbindir}|" \
%{buildroot}%{_initrddir}/%{name}-game-server


chmod 755 %{buildroot}%{_initrddir}/%{name}-game-server

#
# Icons
install -m644 %{SOURCE3} -D %{buildroot}%{_miconsdir}/doom2-newcaco.png
install -m644 %{SOURCE4} -D %{buildroot}%{_iconsdir}/doom2-newcaco.png
install -m644 %{SOURCE5} -D %{buildroot}%{_liconsdir}/doom2-newcaco.png

#
# Menus

install -d %{buildroot}%{_menudir}

cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}): needs="x11" \
		   section="More Applications/Games/Arcade" \
		   title="PrBooM" \
		   longtitle="%{Summary}" \
		   icon="doom2-newcaco.png" \
		   command="%{_gamesbindir}/%{name}"
?package(%{name}): needs="x11" \
		   section="More Applications/Games/Arcade" \
		   title="PrBooM Multiplayer" \
		   longtitle="%{Summary}" \
		   icon="doom2-newcaco.png" \
		   command="%{_gamesbindir}/%{name} -net \`hostname\`"
#?package(%{name}): needs="x11" \
#		    section="Documentation/Websites" \
#		    title="PrBooM Homepage" \
#		    icon="doom2-newcaco.png" \
#		    command="if ps U \$USER | grep -q \$BROWSER; then \$BROWSER -remote \'openURL(%{url})\'; else \$BROWSER \'%{url}\'; fi"
EOF

cat << EOF > %{buildroot}%{_menudir}/%{name}-gl
?package(%{name}-gl): needs="x11" \
		      section="More Applications/Games/Arcade" \
		      title="PrBooM-GL" \
		      longtitle="%{Summary}" \
		      icon="doom2-newcaco.png" \
		      command="%{_gamesbindir}/%{name}-gl"
?package(%{name}-gl): needs="x11" \
		      section="More applications/Games/Arcade" \
		      title="PrBooM-GL Multiplayer" \
		      longtitle="%{Summary}" \
		      icon="doom2-newcaco.png" \
		      command="%{_gamesbindir}/%{name}-gl -net \`hostname\`"
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%post gl
%{update_menus}

%postun gl
%{clean_menus}

%post server
%_post_service %{name}-game-server

%preun server
%_preun_service %{name}-game-server

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc AUTHORS NEWS README TODO
%doc doc/*.txt doc/README.*
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/doom
%{_gamesdatadir}/doom/%{name}.wad
%{_mandir}/man5/*
%{_mandir}/man6/%{name}.6*
%{_menudir}/%{name}
%{_iconsdir}/doom2-newcaco.png
%{_miconsdir}/doom2-newcaco.png
%{_liconsdir}/doom2-newcaco.png

%files gl
%defattr(-,root,root)
%{_gamesbindir}/%{name}-gl
%{_menudir}/%{name}-gl

%files server
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-game-server
%{_initrddir}/%{name}-game-server
%{_gamesbindir}/%{name}-game-server
%{_mandir}/man6/%{name}-game-server*


