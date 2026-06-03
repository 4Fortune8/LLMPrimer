"""Context compression. We use model-generated summarisation as the compressor.

IMPORTANT METHODOLOGICAL NOTE (read before trusting your numbers):
Do NOT hand-write the summary so that it conveniently drops exactly the working
mode your primer restores — that would make the result circular. Use a generic,
faithful summariser (below) that is told to preserve task-relevant facts, and let
it lose the 'how' on its own. The whole hypothesis is that neutral compression
*naturally* dilutes diffuse behavioural conditioning while keeping facts; rig the
compressor and you prove nothing.
"""

SUMMARISE_SYSTEM = (
    "You compress technical context. Preserve all task-relevant facts, problem "
    "statements, and concrete results. Be faithful and neutral. Do not add advice."
)


def compress_context(lm, context_text, ratio):
    target_words = max(20, int(len(context_text.split()) * ratio))
    user = (
        f"Summarise the following so it can stand in for the original in about "
        f"{target_words} words. Keep facts; drop redundancy.\n\n{context_text}"
    )
    ids = lm.render(SUMMARISE_SYSTEM, user)
    # plain generation, no primers
    return lm.generate(ids).strip()
