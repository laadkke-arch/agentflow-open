to_entries | map({
    page_content: .value.page_data,
    metadata: (.value | {
        source: "/content/json_data.json",
        page_name,
        page_url
    } + {seq_num:(.key+1)})
})
