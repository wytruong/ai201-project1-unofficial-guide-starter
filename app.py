import gradio as gr
from embed import embed_and_store
from generate import ask

print("Loading vector store...")
collection, model = embed_and_store()

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question, collection, model)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="UCI Unofficial Guide") as demo:
    gr.Markdown("## UCI Unofficial Guide\nAsk questions about internships, professors, and recruiting at UCI.")
    inp = gr.Textbox(label="Your question", placeholder="e.g. When should I start applying for internships?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=3)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()