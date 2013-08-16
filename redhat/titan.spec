%define __jar_repack 0
%define payload_dir redhat/payload

Name:           titan
Version:        0.4.0
Release:        0.1.snap
Summary:        Titan Distributed Graph Database

Group:          Applications/Databases
License:        ASL 2.0
URL:            http://titan.thinkaurelius.com/
Source0:        http://s3.thinkaurelius.com/downloads/titan/titan-all-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
Titan is a scalable graph database optimized for storing and querying
graphs containing hundreds of billions of vertices and edges
distributed across a multi-machine cluster. Titan is a transactional
database that can support thousands of concurrent users executing
complex graph traversals.

%package cassandra
Summary:        Cassandra graph storage for Titan
Group:          Applications/Databases
%description cassandra
Cassandra backend storage module for Titan

%package hbase
Summary:        HBase graph storage for Titan
Group:          Applications/Databases
%description hbase
HBase backend storage module for Titan

%package berkeleyje
Summary:        BerkeleyDB Java Edition graph storage for Titan
Group:          Applications/Databases
%description berkeleyje
BerkeleyDB Java Edition (BDB JE) backend storage module for Titan

%package persistit
Summary:        Persistit graph storage for Titan
Group:          Applications/Databases
%description persistit
Persistit backend storage module for Titan

%package es
Summary:        Elasticsearch graph indexing for Titan
Group:          Applications/Databases
Requires:       titan-lucene
%description es
Elasticsearch indexing module for Titan

%package lucene
Summary:        Lucene graph indexing for Titan
Group:          Applications/Databases
%description lucene
Lucene indexing module for Titan


%prep

%build
cd %{name}-%{version}
mvn clean install -DskipTests=true
cd titan-dist/titan-dist-all/
mvn clean package -Dgpg.skip=true -Ptitan-release -DskipTests=true
cd - >/dev/null
pkgcommon/bin/partition-jars.sh


%check



%install
cd %{name}-%{version}

# create directory structure
mkdir -p "$RPM_BUILD_ROOT"/etc/default
mkdir -p "$RPM_BUILD_ROOT"/etc/rc.d/init.d
mkdir -p "$RPM_BUILD_ROOT"/etc/titan
mkdir -p "$RPM_BUILD_ROOT"/etc/titan/env.d
mkdir -p "$RPM_BUILD_ROOT"/usr/bin
mkdir -p "$RPM_BUILD_ROOT"/usr/sbin
mkdir -p "$RPM_BUILD_ROOT"/usr/share/doc/%{name}-%{version}
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/berkeleyje
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/cassandra
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/hbase
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/persistit
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/es
mkdir -p "$RPM_BUILD_ROOT"/usr/share/titan/lib/lucene

# copy files
pkgcommon/bin/install-payload.sh "$RPM_BUILD_ROOT"/
cp %{payload_dir}/titan.init "$RPM_BUILD_ROOT"/etc/rc.d/init.d/titan
cp %{payload_dir}/titan.sysconfig "$RPM_BUILD_ROOT"/etc/default/titan

# executables
#cp %{payload_dir}/rexster-console.sh "$RPM_BUILD_ROOT"/usr/bin/
#cp %{payload_dir}/titan "$RPM_BUILD_ROOT"/usr/sbin/
##cp %{payload_dir}/upgrade010to020 "$RPM_BUILD_ROOT"/usr/sbin/titan_upgrade010to020

# configs
##'cp %{payload_dir}/*.local "$RPM_BUILD_ROOT"/etc/titan/
#cp %{payload_dir}/config.properties "$RPM_BUILD_ROOT"/etc/titan/
#cp %{payload_dir}/rexster.xml "$RPM_BUILD_ROOT"/etc/titan/
#cp %{payload_dir}/cassandra.yaml "$RPM_BUILD_ROOT"/etc/titan/
#cp %{payload_dir}/titan-env.sh "$RPM_BUILD_ROOT"/etc/titan/
#cp %{payload_dir}/titan.in.sh "$RPM_BUILD_ROOT"/usr/share/titan/
#cp %{payload_dir}/env.d/* "$RPM_BUILD_ROOT"/etc/titan/env.d/

# init.d
#cp %{payload_dir}/titan.init "$RPM_BUILD_ROOT"/etc/rc.d/init.d/titan
#cp %{payload_dir}/titan.default "$RPM_BUILD_ROOT"/etc/default/titan

# jars
pkgcommon/bin/install-jars.sh "$RPM_BUILD_ROOT"/usr/share/titan/lib'${m:+/$m}'
#modules="berkeleyje cassandra hbase persistit es lucene"
#for m in $modules; do
#    for j in `cat dep-$m.txt | sed -r 's/(.+):(.+):(.+):(.+):(.+)/\2-\4.\3/'`; do
#	mv titan-dist/titan-dist-all/target/titan-all-*/titan-all-*/lib/$j "$RPM_BUILD_ROOT"/usr/share/titan/lib/$m || \
#	    echo "Warning: dependency $j not found" >&2
#    done
#done
#cp titan-dist/titan-dist-all/target/titan-all-*/titan-all-*/lib/*.jar "$RPM_BUILD_ROOT"/usr/share/titan/lib/

# docs
#mv doc/ "$RPM_BUILD_ROOT"/usr/share/doc/titan-%{version}/
#mv CHANGELOG.textile "$RPM_BUILD_ROOT"/usr/share/doc/titan-%{version}/CHANGES.txt
#mv LICENSE.txt "$RPM_BUILD_ROOT"/usr/share/doc/titan-%{version}/
## TODO: NEWS.txt ?
#mv NOTICE.txt "$RPM_BUILD_ROOT"/usr/share/doc/titan-%{version}/
#mv README.txt "$RPM_BUILD_ROOT"/usr/share/doc/titan-%{version}/README.txt
for x in CHANGELOG.textile LICENSE.txt NOTICE.txt README.txt UPGRADE.textile; do
    cp titan-dist/titan-dist-all/target/titan-all-*/titan-all-*/$x  "$RPM_BUILD_ROOT"/usr/share/doc/%{name}-%{version}/
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#%doc CHANGELOG.textile LICENSE.txt NOTICE.txt README.txt UPGRADE.textile doc/
%doc /usr/share/doc/%{name}-%{version}/CHANGELOG.textile
%doc /usr/share/doc/%{name}-%{version}/LICENSE.txt
%doc /usr/share/doc/%{name}-%{version}/NOTICE.txt
%doc /usr/share/doc/%{name}-%{version}/README.txt
%doc /usr/share/doc/%{name}-%{version}/UPGRADE.textile
%attr(0644, root, root) %config /etc/titan/config.properties
%attr(0644, root, root) %config /etc/titan/rexster.xml
%attr(0644, root, root) %config /etc/titan/titan-env.sh
%attr(0644, root, root) %config /etc/default/titan
%attr(0644, root, root) %config /etc/rc.d/init.d/titan
%attr(0755, root, root) %dir /etc/titan/env.d/
%attr(0444, root, root) /etc/titan/env.d/README.txt
%attr(0755, root, root) /usr/bin/rexster-console.sh
%attr(0755, root, root) /usr/sbin/titan
#%attr(0755, root, root) /usr/sbin/titan_upgrade010to020
%attr(0444, root, root) /usr/share/titan/lib/*.jar
%attr(0644, root, root) /usr/share/titan/titan.in.sh


%files berkeleyje
%attr(0644, root, root) %dir /etc/titan/env.d/10-berkeleyje.sh.in
%attr(0444, root, root) /usr/share/titan/lib/berkeleyje/*.jar

%files cassandra
%attr(0644, root, root) %dir /etc/titan/env.d/10-cassandra.sh.in
%attr(0644, root, root) %config /etc/titan/cassandra.yaml
%attr(0444, root, root) /usr/share/titan/lib/cassandra/*.jar

%files hbase
%attr(0644, root, root) %dir /etc/titan/env.d/10-hbase.sh.in
%attr(0444, root, root) /usr/share/titan/lib/hbase/*.jar

%files persistit
%attr(0644, root, root) %dir /etc/titan/env.d/10-persistit.sh.in
%attr(0444, root, root) /usr/share/titan/lib/persistit/*.jar

%files es
%attr(0644, root, root) %dir /etc/titan/env.d/10-es.sh.in
%attr(0444, root, root) /usr/share/titan/lib/es/*.jar

%files lucene
%attr(0644, root, root) %dir /etc/titan/env.d/10-lucene.sh.in
%attr(0444, root, root) /usr/share/titan/lib/lucene/*.jar


%changelog
