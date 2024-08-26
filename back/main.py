from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from graphene import Schema
from schema import Query, Mutation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = Schema(query=Query, mutation=Mutation)

@app.post("/graphql")
async def graphql_server(request: Request):
    data = await request.json()
    query = data.get("query")
    variables = data.get("variables", {})
    result = await schema.execute_async(query, variable_values=variables)

    response = {
        "data": result.data,
    }

    if result.errors:
        response["errors"] = [str(error) for error in result.errors]

    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
