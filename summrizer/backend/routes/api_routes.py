"""
API Routes for CarryOn Summary
Handles all API endpoints and business logic
"""
from flask import Blueprint, request, jsonify
from backend.services.summarizer_service import summarizer_service

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/summarize', methods=['POST'])
def summarize():
    """
    Text summarization endpoint
    
    Request body:
    {
        "text": "Text to summarize",
        "target_sentences": 16  // optional, null for auto-size
    }
    
    Response:
    {
        "summary": "Summarized text",
        "meta": {
            "words_total": 1234,
            "chunks": 2,
            "target_sentences": 16
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Text is required',
                'code': 'MISSING_TEXT'
            }), 400
        
        text = data['text']
        target_sentences = data.get('target_sentences')
        
        # Validate text content
        if not text or not text.strip():
            return jsonify({
                'error': 'Text cannot be empty',
                'code': 'EMPTY_TEXT'
            }), 400
        
        # Validate target_sentences parameter
        if target_sentences is not None:
            if not isinstance(target_sentences, int) or target_sentences < 4 or target_sentences > 80:
                return jsonify({
                    'error': 'Target sentences must be an integer between 4 and 80',
                    'code': 'INVALID_TARGET_SENTENCES'
                }), 400
        
        # Perform summarization
        summary, meta = summarizer_service.summarize_text(text, target_sentences)
        
        return jsonify({
            'summary': summary,
            'meta': meta,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'code': 'INTERNAL_ERROR'
        }), 500


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CarryOn Summary API',
        'version': '1.0.0'
    })


@api_bp.route('/info', methods=['GET'])
def info():
    """API information endpoint"""
    return jsonify({
        'name': 'CarryOn Summary API',
        'version': '1.0.0',
        'description': 'Text summarization service with extractive algorithm',
        'endpoints': {
            'POST /api/summarize': 'Summarize text content',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        },
        'features': [
            'Auto-size summaries based on content length',
            'Manual target sentence control (4-80)',
            'Hierarchical processing for long texts',
            'Preserves key information and structure'
        ]
    })


@api_bp.route('/stats', methods=['POST'])
def stats():
    """
    Get text statistics without summarizing
    
    Request body:
    {
        "text": "Text to analyze"
    }
    
    Response:
    {
        "words_total": 1234,
        "sentences_total": 45,
        "paragraphs_total": 8,
        "recommended_target": 16
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Text is required',
                'code': 'MISSING_TEXT'
            }), 400
        
        text = data['text']
        
        if not text or not text.strip():
            return jsonify({
                'error': 'Text cannot be empty',
                'code': 'EMPTY_TEXT'
            }), 400
        
        # Calculate statistics
        import re
        words_total = len(re.findall(r"[A-Za-z0-9']+", text))
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", text.strip())
        sentences_total = len([s for s in sentences if s.strip()])
        paragraphs_total = len([p for p in text.split('\n\n') if p.strip()])
        
        # Calculate recommended target
        if words_total <= 180:
            recommended_target = 6
        elif words_total <= 600:
            recommended_target = 12
        elif words_total <= 1500:
            recommended_target = 18
        elif words_total <= 3000:
            recommended_target = 24
        else:
            recommended_target = 32
        
        return jsonify({
            'words_total': words_total,
            'sentences_total': sentences_total,
            'paragraphs_total': paragraphs_total,
            'recommended_target': recommended_target,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'code': 'INTERNAL_ERROR'
        }), 500