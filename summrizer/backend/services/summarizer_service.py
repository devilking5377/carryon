"""
Text Summarization Service
Handles all text summarization logic and processing
"""
import re
from collections import Counter
from typing import List, Tuple, Optional


class SummarizerService:
    """Service class for text summarization operations"""
    
    # Common stopwords for filtering
    STOPWORDS = {
        "a", "an", "the", "and", "or", "but", "if", "while", "with", "without", 
        "of", "to", "in", "on", "for", "from", "by", "as", "at", "that", "this", 
        "these", "those", "it", "its", "is", "are", "was", "were", "be", "been", 
        "being", "has", "have", "had", "do", "does", "did", "can", "could", 
        "should", "would", "may", "might", "must", "will", "just", "also", 
        "not", "no", "nor", "so", "than", "then", "too", "very"
    }
    
    def __init__(self):
        """Initialize the summarizer service"""
        pass
    
    def summarize_text(self, text: str, target_sentences: Optional[int] = 16) -> Tuple[str, dict]:
        """
        Main summarization method
        
        Args:
            text: Input text to summarize
            target_sentences: Target number of sentences (None for auto-size)
            
        Returns:
            Tuple of (summary_text, metadata)
        """
        text = text or ""
        words_total = len(re.findall(r"[A-Za-z0-9']+", text))
        
        if words_total == 0:
            return "", {"words_total": 0, "chunks": 0, "target_sentences": target_sentences or 0}

        if target_sentences is None:
            target_sentences = self._auto_target(words_total)

        if words_total <= 2000:
            # Simple summarization for short texts
            sentences = self._to_sentences(text)
            summary_sentences = self._summarize_sentences(sentences, target_sentences)
            summary = self._to_paragraphs(summary_sentences)
            return summary, {
                "words_total": words_total, 
                "chunks": 1, 
                "target_sentences": target_sentences
            }

        # Hierarchical summarization for long texts
        raw_chunks = self._chunk(text, max_words=1800)
        chunk_summaries: List[str] = []
        
        for chunk in raw_chunks:
            sents = self._to_sentences(chunk)
            chunk_summary_sents = self._summarize_sentences(sents, max(8, target_sentences // 2))
            chunk_summaries.append(" ".join(chunk_summary_sents))
        
        combined = "\n\n".join(chunk_summaries)
        final_sents = self._to_sentences(combined)
        final_summary_sents = self._summarize_sentences(final_sents, target_sentences)
        summary = self._to_paragraphs(final_summary_sents)
        
        return summary, {
            "words_total": words_total, 
            "chunks": len(raw_chunks), 
            "target_sentences": target_sentences
        }
    
    def _to_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        text = re.sub(r"\s+", " ", text or "").strip()
        if not text:
            return []
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", text)
        sentences = [s.strip() for s in parts if s and len(s.strip()) > 1]
        return sentences

    def _normalize(self, word: str) -> str:
        """Normalize word for frequency analysis"""
        return re.sub(r"[^a-z0-9]", "", word.lower())

    def _word_freq(self, words: List[str]) -> Counter:
        """Calculate normalized word frequencies"""
        words_norm = [self._normalize(w) for w in words]
        words_filt = [w for w in words_norm if w and w not in self.STOPWORDS]
        freq = Counter(words_filt)
        
        if not freq:
            return freq
        
        max_f = max(freq.values())
        for k in list(freq.keys()):
            freq[k] = freq[k] / max_f
        return freq

    def _score_sentence(self, sentence: str, freq: Counter) -> float:
        """Score a sentence based on word frequency and other signals"""
        words = re.findall(r"[A-Za-z0-9']+", sentence)
        if not words:
            return 0.0
        
        # Base score from word frequencies
        base = sum(freq.get(self._normalize(w), 0.0) for w in words)
        
        # Bonus points for special patterns
        bonus = 0.0
        for w in words:
            if re.match(r"^[0-9]", w):  # Numbers
                bonus += 0.05
            elif re.match(r"^[A-Z][a-zA-Z0-9]*", w):  # Capitalized words
                bonus += 0.03
        
        # Bonus for lists and structured content
        if re.search(r"(^[-*•]\s)|(:)", sentence):
            bonus += 0.06
        
        return (base + bonus) / (len(words) ** 0.5)

    def _summarize_sentences(self, sentences: List[str], target_count: int) -> List[str]:
        """Select top sentences for summary"""
        if target_count <= 0:
            return []
        if len(sentences) <= target_count:
            return sentences
        
        # Calculate word frequencies
        all_words = []
        for s in sentences:
            all_words.extend(re.findall(r"[A-Za-z0-9']+", s))
        freq = self._word_freq(all_words)
        
        # Score and rank sentences
        scored = [(i, self._score_sentence(s, freq)) for i, s in enumerate(sentences)]
        
        # Select top sentences while preserving original order
        top_idx = sorted(
            sorted(scored, key=lambda x: x[1], reverse=True)[:target_count], 
            key=lambda x: x[0]
        )
        
        return [sentences[i] for i, _ in top_idx]

    def _chunk(self, text: str, max_words: int = 1500) -> List[str]:
        """Split text into chunks for hierarchical processing"""
        words = re.findall(r"[A-Za-z0-9']+|\s+|\S", text)
        chunks: List[str] = []
        current: List[str] = []
        count = 0
        
        for token in words:
            current.append(token)
            if re.match(r"[A-Za-z0-9']+", token):
                count += 1
            if count >= max_words:
                chunks.append("".join(current).strip())
                current = []
                count = 0
        
        if current:
            chunks.append("".join(current).strip())
        
        return chunks

    def _auto_target(self, words_total: int) -> int:
        """Automatically determine target sentence count based on text length"""
        if words_total <= 180:
            return 6
        if words_total <= 600:
            return 12
        if words_total <= 1500:
            return 18
        if words_total <= 3000:
            return 24
        return 32

    def _to_paragraphs(self, sentences: List[str], max_per_para: int = 4) -> str:
        """Group sentences into paragraphs"""
        paras: List[str] = []
        for i in range(0, len(sentences), max_per_para):
            paras.append(" ".join(sentences[i:i + max_per_para]))
        return "\n\n".join(paras)


# Global service instance
summarizer_service = SummarizerService()


def summarize_text(text: str, target_sentences: Optional[int] = 16) -> Tuple[str, dict]:
    """
    Convenience function for backward compatibility
    """
    return summarizer_service.summarize_text(text, target_sentences)