import type { ConfigExternal } from "@orval/core"
import { defineConfig } from "orval"

export default defineConfig({
  vision: {
    input: {
      target: "./src/api/openapi.json",
      validation: false
    },
    output: {
      target: "./src/api/openapi",
      mode: "tags-split",
      client: "react-query",
      headers: true,
      clean: true,
      prettier: true,
      schemas: "src/api/openapi/schemas",
      override: {
        useTypeOverInterfaces: true,
        mutator: {
          path: "./src/api/client.ts",
          name: "customAxios"
        },
        query: {
          useQuery: true,
          useInfinite: true,
          useInfiniteQueryParam: "cursor"
        }
      }
    }
  }
}) as ConfigExternal
