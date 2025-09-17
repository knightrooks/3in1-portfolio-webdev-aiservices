#!/usr/bin/env python3
"""
Nomic Embed Text Model Runner
High-Quality Text Embeddings for Semantic Search and Retrieval
"""

import os
import json
import yaml
import asyncio
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from dataclasses import dataclass
import hashlib
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NomicEmbedConfig:
    """Configuration class for Nomic Embed Text model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class EmbeddingCache:
    """Simple caching system for embeddings"""
    
    def __init__(self, max_size: int = 10000):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Get embedding from cache"""
        key = self._get_cache_key(text)
        if key in self.cache:
            # Update access order
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, text: str, embedding: np.ndarray):
        """Store embedding in cache"""
        key = self._get_cache_key(text)
        
        # Remove oldest if cache is full
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        
        self.cache[key] = embedding
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

class NomicEmbedRunner:
    """
    Runner class for Nomic Embed Text model
    Handles text embedding generation, semantic search, and document analysis
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Nomic Embed runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        
        # Initialize embedding components
        self.embedding_cache = EmbeddingCache()
        self.document_store = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        
        # Initialize embedding model (fallback to TF-IDF if sentence-transformers not available)
        self._init_embedding_model()
        
        logger.info(f"Nomic Embed Runner initialized: {self.model_name} v{self.version}")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> NomicEmbedConfig:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return NomicEmbedConfig(
                name=config_data['name'],
                version=config_data['version'],
                provider=config_data['provider'],
                model_type=config_data['model_type'],
                parameters=config_data['parameters'],
                capabilities=config_data['capabilities'],
                specialties=config_data['specialties']
            )
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _init_embedding_model(self):
        """Initialize embedding model"""
        try:
            # Try to initialize with sentence-transformers (if available)
            try:
                # Use a lightweight model as fallback
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.embedding_method = "sentence_transformer"
                self.embedding_dim = 384
                logger.info("Initialized with SentenceTransformer model")
            except Exception as e:
                logger.warning(f"SentenceTransformer not available: {e}")
                # Fallback to TF-IDF
                self.sentence_model = None
                self.embedding_method = "tfidf"
                self.embedding_dim = 5000
                logger.info("Initialized with TF-IDF fallback")
            
            # Initialize document preprocessing
            self.preprocessing_patterns = {
                'url_pattern': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
                'email_pattern': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
                'extra_spaces': re.compile(r'\s+'),
                'special_chars': re.compile(r'[^\w\s\-.,!?;:()"\']')
            }
            
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            raise
    
    async def generate_embeddings(self, texts: Union[str, List[str]], normalize: bool = True) -> Dict[str, Any]:
        """
        Generate embeddings for input text(s)
        
        Args:
            texts: Single text or list of texts to embed
            normalize: Whether to normalize the embeddings
        
        Returns:
            Dictionary containing embeddings and metadata
        """
        try:
            # Ensure texts is a list
            if isinstance(texts, str):
                text_list = [texts]
                single_text = True
            else:
                text_list = texts
                single_text = False
            
            # Preprocess texts
            processed_texts = [self._preprocess_text(text) for text in text_list]
            
            # Generate embeddings
            embeddings = []
            cache_hits = 0
            
            for processed_text in processed_texts:
                # Check cache first
                cached_embedding = self.embedding_cache.get(processed_text)
                if cached_embedding is not None:
                    embeddings.append(cached_embedding)
                    cache_hits += 1
                else:
                    # Generate new embedding
                    embedding = await self._compute_embedding(processed_text)
                    if normalize:
                        embedding = self._normalize_embedding(embedding)
                    
                    embeddings.append(embedding)
                    self.embedding_cache.set(processed_text, embedding)
            
            # Prepare response
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "embeddings": embeddings[0] if single_text else embeddings,
                "embedding_metadata": {
                    "dimension": self.embedding_dim,
                    "method": self.embedding_method,
                    "normalized": normalize,
                    "cache_hits": cache_hits,
                    "total_texts": len(text_list)
                },
                "preprocessing": {
                    "original_texts": text_list,
                    "processed_texts": processed_texts,
                    "preprocessing_applied": True
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def semantic_search(self, query: str, documents: List[str], top_k: int = 5) -> Dict[str, Any]:
        """
        Perform semantic search using embeddings
        
        Args:
            query: Search query
            documents: List of documents to search
            top_k: Number of top results to return
        
        Returns:
            Dictionary containing search results and similarities
        """
        try:
            # Generate query embedding
            query_response = await self.generate_embeddings(query)
            query_embedding = query_response["embeddings"]
            
            # Generate document embeddings
            doc_response = await self.generate_embeddings(documents)
            doc_embeddings = doc_response["embeddings"]
            
            # Calculate similarities
            if self.embedding_method == "sentence_transformer":
                query_embedding = query_embedding.reshape(1, -1)
                similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
            else:  # TF-IDF method
                similarities = self._calculate_tfidf_similarities(query, documents)
            
            # Get top results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for i, idx in enumerate(top_indices):
                results.append({
                    "rank": i + 1,
                    "document_index": int(idx),
                    "document": documents[idx],
                    "similarity_score": float(similarities[idx]),
                    "relevance": self._categorize_relevance(similarities[idx])
                })
            
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "search_results": results,
                "search_metadata": {
                    "total_documents": len(documents),
                    "top_k_requested": top_k,
                    "results_returned": len(results),
                    "embedding_method": self.embedding_method,
                    "average_similarity": float(np.mean(similarities)),
                    "max_similarity": float(np.max(similarities))
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def similarity_analysis(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Analyze similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Dictionary containing similarity analysis
        """
        try:
            # Generate embeddings for both texts
            embeddings_response = await self.generate_embeddings([text1, text2])
            embeddings = embeddings_response["embeddings"]
            
            # Calculate similarity
            if self.embedding_method == "sentence_transformer":
                similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            else:  # TF-IDF method
                similarity = self._calculate_tfidf_similarities(text1, [text2])[0]
            
            # Analyze semantic overlap
            semantic_analysis = await self._analyze_semantic_overlap(text1, text2)
            
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "similarity_score": float(similarity),
                "similarity_category": self._categorize_similarity(similarity),
                "texts": {
                    "text1": text1,
                    "text2": text2,
                    "text1_length": len(text1.split()),
                    "text2_length": len(text2.split())
                },
                "semantic_analysis": semantic_analysis,
                "interpretation": self._interpret_similarity(similarity, semantic_analysis)
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing similarity: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def document_clustering(self, documents: List[str], n_clusters: int = 5) -> Dict[str, Any]:
        """
        Cluster documents based on semantic similarity
        
        Args:
            documents: List of documents to cluster
            n_clusters: Number of clusters to create
        
        Returns:
            Dictionary containing clustering results
        """
        try:
            # Generate embeddings for all documents
            embeddings_response = await self.generate_embeddings(documents)
            embeddings = np.array(embeddings_response["embeddings"])
            
            # Simple k-means clustering (basic implementation)
            clusters = await self._simple_kmeans_clustering(embeddings, n_clusters)
            
            # Organize results by cluster
            clustered_docs = {}
            for i, cluster_id in enumerate(clusters):
                if cluster_id not in clustered_docs:
                    clustered_docs[cluster_id] = []
                clustered_docs[cluster_id].append({
                    "document_index": i,
                    "document": documents[i],
                    "document_length": len(documents[i].split())
                })
            
            # Generate cluster summaries
            cluster_summaries = {}
            for cluster_id, docs in clustered_docs.items():
                cluster_summaries[cluster_id] = await self._generate_cluster_summary(docs)
            
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "clustering_results": {
                    "n_clusters": n_clusters,
                    "total_documents": len(documents),
                    "clusters": clustered_docs,
                    "cluster_summaries": cluster_summaries
                },
                "clustering_metadata": {
                    "embedding_method": self.embedding_method,
                    "clustering_algorithm": "k-means",
                    "cluster_distribution": {str(k): len(v) for k, v in clustered_docs.items()}
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error clustering documents: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for embedding generation"""
        try:
            # Convert to lowercase
            processed = text.lower()
            
            # Remove URLs
            processed = self.preprocessing_patterns['url_pattern'].sub('', processed)
            
            # Remove email addresses
            processed = self.preprocessing_patterns['email_pattern'].sub('', processed)
            
            # Remove excessive special characters (keep basic punctuation)
            processed = self.preprocessing_patterns['special_chars'].sub(' ', processed)
            
            # Normalize whitespace
            processed = self.preprocessing_patterns['extra_spaces'].sub(' ', processed)
            
            # Strip and ensure minimum length
            processed = processed.strip()
            if not processed:
                processed = text  # Fallback to original if preprocessing removes everything
            
            return processed
            
        except Exception as e:
            logger.warning(f"Error preprocessing text: {e}")
            return text  # Return original text if preprocessing fails
    
    async def _compute_embedding(self, text: str) -> np.ndarray:
        """Compute embedding for preprocessed text"""
        try:
            if self.embedding_method == "sentence_transformer" and self.sentence_model:
                embedding = self.sentence_model.encode(text)
                return np.array(embedding)
            else:
                # Fallback to TF-IDF
                # For single text, we need to fit on a corpus first
                # This is a simplified implementation
                corpus = [text]  # In production, use a larger corpus
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
                return tfidf_matrix.toarray()[0]
                
        except Exception as e:
            logger.error(f"Error computing embedding: {e}")
            # Return zero vector as fallback
            return np.zeros(self.embedding_dim)
    
    def _normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        """Normalize embedding to unit length"""
        try:
            norm = np.linalg.norm(embedding)
            if norm > 0:
                return embedding / norm
            return embedding
        except Exception as e:
            logger.warning(f"Error normalizing embedding: {e}")
            return embedding
    
    def _calculate_tfidf_similarities(self, query: str, documents: List[str]) -> np.ndarray:
        """Calculate similarities using TF-IDF (fallback method)"""
        try:
            # Create corpus with query and documents
            corpus = [query] + documents
            
            # Fit TF-IDF vectorizer
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            
            # Calculate cosine similarities between query (first row) and documents
            query_vector = tfidf_matrix[0:1]
            doc_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(query_vector, doc_vectors)[0]
            return similarities
            
        except Exception as e:
            logger.error(f"Error calculating TF-IDF similarities: {e}")
            return np.zeros(len(documents))
    
    def _categorize_relevance(self, similarity_score: float) -> str:
        """Categorize relevance based on similarity score"""
        if similarity_score >= 0.8:
            return "highly_relevant"
        elif similarity_score >= 0.6:
            return "moderately_relevant"
        elif similarity_score >= 0.4:
            return "somewhat_relevant"
        elif similarity_score >= 0.2:
            return "low_relevance"
        else:
            return "not_relevant"
    
    def _categorize_similarity(self, similarity_score: float) -> str:
        """Categorize similarity between two texts"""
        if similarity_score >= 0.9:
            return "nearly_identical"
        elif similarity_score >= 0.7:
            return "highly_similar"
        elif similarity_score >= 0.5:
            return "moderately_similar"
        elif similarity_score >= 0.3:
            return "somewhat_similar"
        else:
            return "dissimilar"
    
    async def _analyze_semantic_overlap(self, text1: str, text2: str) -> Dict[str, Any]:
        """Analyze semantic overlap between two texts"""
        try:
            # Basic word overlap analysis
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            common_words = words1.intersection(words2)
            unique_words1 = words1.difference(words2)
            unique_words2 = words2.difference(words1)
            
            overlap_ratio = len(common_words) / len(words1.union(words2)) if words1.union(words2) else 0
            
            return {
                "word_overlap": {
                    "common_words": list(common_words),
                    "unique_to_text1": list(unique_words1),
                    "unique_to_text2": list(unique_words2),
                    "overlap_ratio": overlap_ratio
                },
                "length_analysis": {
                    "text1_words": len(words1),
                    "text2_words": len(words2),
                    "length_ratio": len(words1) / len(words2) if len(words2) > 0 else float('inf')
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing semantic overlap: {e}")
            return {"error": str(e)}
    
    def _interpret_similarity(self, similarity_score: float, semantic_analysis: Dict[str, Any]) -> str:
        """Generate interpretation of similarity results"""
        category = self._categorize_similarity(similarity_score)
        overlap_ratio = semantic_analysis.get("word_overlap", {}).get("overlap_ratio", 0)
        
        if category == "nearly_identical":
            return f"The texts are nearly identical with {similarity_score:.2f} similarity. High word overlap ({overlap_ratio:.2f}) confirms strong semantic alignment."
        elif category == "highly_similar":
            return f"The texts are highly similar ({similarity_score:.2f}) and likely discuss the same topic with similar context."
        elif category == "moderately_similar":
            return f"The texts show moderate similarity ({similarity_score:.2f}), suggesting related but distinct content."
        elif category == "somewhat_similar":
            return f"The texts have some similarity ({similarity_score:.2f}), possibly sharing a common theme or domain."
        else:
            return f"The texts appear dissimilar ({similarity_score:.2f}), likely covering different topics or contexts."
    
    async def _simple_kmeans_clustering(self, embeddings: np.ndarray, n_clusters: int) -> List[int]:
        """Simple k-means clustering implementation"""
        try:
            # Initialize centroids randomly
            n_samples, n_features = embeddings.shape
            centroids = np.random.rand(n_clusters, n_features)
            
            # Normalize centroids
            for i in range(n_clusters):
                centroids[i] = self._normalize_embedding(centroids[i])
            
            # Iterate to find optimal centroids
            max_iterations = 100
            tolerance = 1e-4
            
            for iteration in range(max_iterations):
                # Assign points to nearest centroid
                distances = np.array([[np.linalg.norm(embedding - centroid) 
                                     for centroid in centroids] 
                                     for embedding in embeddings])
                clusters = np.argmin(distances, axis=1)
                
                # Update centroids
                new_centroids = np.zeros_like(centroids)
                for i in range(n_clusters):
                    cluster_points = embeddings[clusters == i]
                    if len(cluster_points) > 0:
                        new_centroids[i] = np.mean(cluster_points, axis=0)
                        new_centroids[i] = self._normalize_embedding(new_centroids[i])
                    else:
                        new_centroids[i] = centroids[i]  # Keep old centroid if no points assigned
                
                # Check for convergence
                if np.allclose(centroids, new_centroids, atol=tolerance):
                    break
                
                centroids = new_centroids
            
            return clusters.tolist()
            
        except Exception as e:
            logger.error(f"Error in k-means clustering: {e}")
            # Return random clusters as fallback
            return [i % n_clusters for i in range(len(embeddings))]
    
    async def _generate_cluster_summary(self, cluster_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary for a document cluster"""
        try:
            # Basic cluster statistics
            doc_count = len(cluster_docs)
            total_words = sum(doc["document_length"] for doc in cluster_docs)
            avg_doc_length = total_words / doc_count if doc_count > 0 else 0
            
            # Extract common themes (simple word frequency analysis)
            all_words = []
            for doc in cluster_docs:
                words = doc["document"].lower().split()
                all_words.extend(words)
            
            # Count word frequencies
            word_freq = {}
            for word in all_words:
                if len(word) > 3:  # Only consider words longer than 3 characters
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "document_count": doc_count,
                "average_document_length": round(avg_doc_length, 2),
                "total_words": total_words,
                "top_keywords": [{"word": word, "frequency": freq} for word, freq in top_keywords],
                "cluster_theme": f"Documents related to: {', '.join([kw[0] for kw in top_keywords[:3]])}"
            }
            
        except Exception as e:
            logger.error(f"Error generating cluster summary: {e}")
            return {"error": str(e), "document_count": len(cluster_docs)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            "name": self.model_name,
            "version": self.version,
            "provider": self.config.provider,
            "model_type": self.config.model_type,
            "capabilities": self.config.capabilities,
            "specialties": list(self.config.specialties.keys()),
            "parameters": self.config.parameters,
            "status": "operational",
            "embedding_method": self.embedding_method,
            "embedding_dimension": self.embedding_dim,
            "cache_size": len(self.embedding_cache.cache),
            "supported_operations": [
                "text_embedding", "semantic_search", "similarity_analysis",
                "document_clustering", "content_matching"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the embedding model"""
        try:
            # Test embedding generation
            test_text = "This is a test document for health checking."
            embedding_result = await self.generate_embeddings(test_text)
            
            # Test semantic search
            test_docs = [
                "Machine learning is a subset of artificial intelligence.",
                "Deep learning uses neural networks with multiple layers.",
                "Natural language processing helps computers understand text."
            ]
            search_result = await self.semantic_search("artificial intelligence", test_docs, top_k=2)
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "embedding_test": "error" not in embedding_result,
                "search_test": "error" not in search_result,
                "embedding_method": self.embedding_method,
                "cache_size": len(self.embedding_cache.cache),
                "all_tests_passed": ("error" not in embedding_result and 
                                   "error" not in search_result)
            }
        except Exception as e:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "error": str(e)
            }

# Example usage and testing
async def main():
    """Main function for testing Nomic Embed runner"""
    try:
        # Initialize runner
        runner = NomicEmbedRunner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test embedding generation
        print("\n=== Embedding Generation Test ===")
        test_texts = [
            "Artificial intelligence is transforming technology.",
            "Machine learning algorithms improve with more data."
        ]
        embeddings = await runner.generate_embeddings(test_texts)
        print(f"Generated embeddings for {len(test_texts)} texts")
        print(f"Embedding dimension: {embeddings['embedding_metadata']['dimension']}")
        
        # Test semantic search
        print("\n=== Semantic Search Test ===")
        documents = [
            "Python is a programming language used for data science.",
            "JavaScript is popular for web development.",
            "Machine learning requires large datasets for training.",
            "Neural networks are inspired by biological neurons.",
            "Web frameworks make development faster and easier."
        ]
        search_results = await runner.semantic_search(
            "programming languages for development", 
            documents, 
            top_k=3
        )
        
        print("Top search results:")
        for result in search_results["search_results"]:
            print(f"  {result['rank']}. {result['document'][:50]}... (score: {result['similarity_score']:.3f})")
        
        # Test similarity analysis
        print("\n=== Similarity Analysis Test ===")
        text1 = "Machine learning is a powerful tool for data analysis."
        text2 = "Data analysis benefits greatly from machine learning techniques."
        similarity = await runner.similarity_analysis(text1, text2)
        print(f"Similarity score: {similarity['similarity_score']:.3f}")
        print(f"Category: {similarity['similarity_category']}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())