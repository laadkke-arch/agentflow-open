set -e
for item in 'momepy momepy docs' 'libpysal libpysal docs notebooks' 'dask-geopandas dask_geopandas doc'; do
    read -r -a args <<< "$item"
    repo="${args[0]}"
    cd "/tmp/af091-sources/$repo"
    paths=()
    for path in "${args[@]:1}"; do
        if test -d "$path"; then paths+=("$path"); fi
    done
    {
        git show -s --format='commit %H%nrevision_date %cI' HEAD
        date -u +'%Y-%m-%dT%H:%M:%SZ'
        printf 'roots %s\n' "${paths[*]}"
        printf 'types and named literals\n'
        rg -n -o --sort path -g '*.py' -g '*.rst' -g '*.md' -g '*.ipynb' '(?i)geom_type[s]?|geometry_type[s]?|geometry\.type|(?:shapely\.)?get_type_id|GeometryType\.POINT|[\x22\x27]Point[\x22\x27]|[\x22\x27]Point[\\][\x22]' "${paths[@]}"
        printf 'spatial selectors and partition filters\n'
        rg -n -o --sort path -g '*.py' -g '*.rst' -g '*.md' -g '*.ipynb' '\.intersects\(|predicate\s*=\s*(?:\\)?[\x22\x27]intersects|\.cx\[|\bsjoin\(' "${paths[@]}"
    } > "/tmp/af091-lab/search/$repo.txt"
done
