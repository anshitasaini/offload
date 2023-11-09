import { cn } from "@/lib/utils"
import { PersonIcon } from "@radix-ui/react-icons"
import remarkGfm from "remark-gfm"

import type { ChatMessageSchema } from "~api/openapi/schemas"

import { MemoizedReactMarkdown } from "./markdown"
import { Separator } from "./ui/separator"

const ChatMessage = ({ message, sender }: ChatMessageSchema) => {
  return (
    <div className={cn("group relative mb-2 flex items-start")}>
      <div
        className={cn(
          "flex h-6 w-6 shrink-0 select-none items-center justify-center rounded-md border shadow bg-background"
        )}>
        <PersonIcon />
      </div>
      <div className="flex-1 px-1 ml-3 space-y-2 overflow-hidden">
        <MemoizedReactMarkdown
          className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0"
          components={{
            p({ children }) {
              return <p className="mb-2 last:mb-0">{children}</p>
            }
          }}>
          {message}
        </MemoizedReactMarkdown>
        {/* <MemoizedReactMarkdown
          className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0"
          remarkPlugins={[remarkGfm]}
          components={{
            p({ children }) {
              return <p className="mb-2 last:mb-0">{children}</p>
            },
            code({ node, inline, className, children, ...props }) {
              if (children.length) {
                if (children[0] == "▍") {
                  return (
                    <span className="mt-1 cursor-default animate-pulse">▍</span>
                  )
                }

                children[0] = (children[0] as string).replace("`▍`", "▍")
              }

              const match = /language-(\w+)/.exec(className || "")

              if (inline) {
                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              }

              return (
                <div></div>
                // <CodeBlock
                //   key={Math.random()}
                //   language={(match && match[1]) || ""}
                //   value={String(children).replace(/\n$/, "")}
                //   {...props}
                // />
              )
            }
          }}>
          {message.content}
        </MemoizedReactMarkdown> */}
      </div>
    </div>
  )
}

export default ChatMessage
