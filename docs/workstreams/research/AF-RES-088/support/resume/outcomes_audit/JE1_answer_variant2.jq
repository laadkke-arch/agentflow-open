to_entries | map((.value | {
    page_content: .page_data,
    metadata: {
        source: "/content/json_data.json",
        page_name,
        page_url
    }
}) * { metadata: { seq_num: (.key+1) } })
