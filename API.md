POST /record 
{
    prod_id: identifier,
    index: index in blockchain,
    content: {
        prod_id: identifier,
        //content depending on form 
    }

}

POST /form
{
    company_id: indentifier,
    index: index in blockchain,
    content: {
        company_id: indetifier,
        //content depending on form
    }
}

GET /record
query = {
    prod_id,
    date,
}
response = {
    index
}

GET /form 
query = {
    company_id,
    name
}
response = {
    index
}