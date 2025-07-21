# src/language_support.py
from typing import Dict, List, Optional
import json
import os

class LanguageManager:
    def __init__(self):
        self.supported_languages = {
            "en": "English",
            "es": "Español",
            "fr": "Français",
            "de": "Deutsch",
            "pt": "Português",
            "it": "Italiano",
            "zh": "中文",
            "ja": "日本語",
            "ko": "한국어",
            "ar": "العربية",
            "hi": "हिन्दी",
            "ru": "Русский"
        }
        
        self.translations = self._load_translations()
        self.default_language = "en"
    
    def _load_translations(self) -> Dict:
        """Load all language translations"""
        translations = {}
        
        # UI Translations
        ui_translations = {
            "en": {
                "app_title": "🌱 LeafGuard AI",
                "app_subtitle": "AI-Powered Plant Disease Detection & Analysis",
                "app_description": "Advanced plant health diagnostics for farmers and agricultural professionals",
                "upload_title": "📤 Upload Plant Images",
                "upload_description": "Upload one or multiple leaf images for disease analysis. Supported formats: JPG, PNG, JPEG",
                "choose_files": "Choose files",
                "analysis_results": "🔍 Analysis Results",
                "processing": "Processing",
                "analysis_complete": "✅ Analysis complete for",
                "download_report": "📄 Download LeafGuard Report",
                "report_generated": "📊 Report generated with disease classification and severity analysis",
                "error_processing": "❌ Error processing",
                "all_processed": "🎉 All images processed successfully!",
                "about_title": "🚀 About LeafGuard AI",
                "about_description": "LeafGuard AI uses advanced machine learning to:",
                "features_title": "📋 Supported Features",
                "detect_diseases": "🔍 Detect plant diseases with high accuracy",
                "estimate_severity": "📊 Estimate disease severity levels",
                "generate_heatmaps": "🗺️ Generate visual heatmaps for analysis",
                "create_reports": "📋 Create detailed PDF reports",
                "store_results": "💾 Store results for future reference",
                "batch_upload": "Batch image upload",
                "multiple_classification": "Multiple disease classification",
                "severity_estimation": "Severity estimation",
                "grad_cam_heatmaps": "Grad-CAM heatmaps",
                "pdf_reports": "PDF report generation",
                "database_storage": "Database storage",
                "footer_text": "🌱 LeafGuard AI - Protecting crops with intelligent monitoring",
                "footer_subtext": "Advanced plant disease detection powered by AI"
            },
            "es": {
                "app_title": "🌱 LeafGuard AI",
                "app_subtitle": "Detección y Análisis de Enfermedades Vegetales con IA",
                "app_description": "Diagnóstico avanzado de salud vegetal para agricultores y profesionales agrícolas",
                "upload_title": "📤 Subir Imágenes de Plantas",
                "upload_description": "Sube una o múltiples imágenes de hojas para análisis de enfermedades. Formatos soportados: JPG, PNG, JPEG",
                "choose_files": "Seleccionar archivos",
                "analysis_results": "🔍 Resultados del Análisis",
                "processing": "Procesando",
                "analysis_complete": "✅ Análisis completado para",
                "download_report": "📄 Descargar Reporte LeafGuard",
                "report_generated": "📊 Reporte generado con clasificación de enfermedades y análisis de severidad",
                "error_processing": "❌ Error procesando",
                "all_processed": "🎉 ¡Todas las imágenes procesadas exitosamente!",
                "about_title": "🚀 Acerca de LeafGuard AI",
                "about_description": "LeafGuard AI utiliza aprendizaje automático avanzado para:",
                "features_title": "📋 Características Soportadas",
                "detect_diseases": "🔍 Detectar enfermedades vegetales con alta precisión",
                "estimate_severity": "📊 Estimar niveles de severidad de enfermedades",
                "generate_heatmaps": "🗺️ Generar mapas de calor visuales para análisis",
                "create_reports": "📋 Crear reportes PDF detallados",
                "store_results": "💾 Almacenar resultados para referencia futura",
                "batch_upload": "Carga por lotes de imágenes",
                "multiple_classification": "Clasificación múltiple de enfermedades",
                "severity_estimation": "Estimación de severidad",
                "grad_cam_heatmaps": "Mapas de calor Grad-CAM",
                "pdf_reports": "Generación de reportes PDF",
                "database_storage": "Almacenamiento en base de datos",
                "footer_text": "🌱 LeafGuard AI - Protegiendo cultivos con monitoreo inteligente",
                "footer_subtext": "Detección avanzada de enfermedades vegetales potenciada por IA"
            },
            "fr": {
                "app_title": "🌱 LeafGuard AI",
                "app_subtitle": "Détection et Analyse des Maladies Végétales par IA",
                "app_description": "Diagnostic avancé de la santé végétale pour les agriculteurs et professionnels agricoles",
                "upload_title": "📤 Télécharger des Images de Plantes",
                "upload_description": "Téléchargez une ou plusieurs images de feuilles pour l'analyse des maladies. Formats supportés: JPG, PNG, JPEG",
                "choose_files": "Choisir des fichiers",
                "analysis_results": "🔍 Résultats de l'Analyse",
                "processing": "Traitement",
                "analysis_complete": "✅ Analyse terminée pour",
                "download_report": "📄 Télécharger le Rapport LeafGuard",
                "report_generated": "📊 Rapport généré avec classification des maladies et analyse de sévérité",
                "error_processing": "❌ Erreur lors du traitement",
                "all_processed": "🎉 Toutes les images traitées avec succès !",
                "about_title": "🚀 À Propos de LeafGuard AI",
                "about_description": "LeafGuard AI utilise l'apprentissage automatique avancé pour :",
                "features_title": "📋 Fonctionnalités Supportées",
                "detect_diseases": "🔍 Détecter les maladies végétales avec une haute précision",
                "estimate_severity": "📊 Estimer les niveaux de sévérité des maladies",
                "generate_heatmaps": "🗺️ Générer des cartes de chaleur visuelles pour l'analyse",
                "create_reports": "📋 Créer des rapports PDF détaillés",
                "store_results": "💾 Stocker les résultats pour référence future",
                "batch_upload": "Téléchargement par lots d'images",
                "multiple_classification": "Classification multiple des maladies",
                "severity_estimation": "Estimation de la sévérité",
                "grad_cam_heatmaps": "Cartes de chaleur Grad-CAM",
                "pdf_reports": "Génération de rapports PDF",
                "database_storage": "Stockage en base de données",
                "footer_text": "🌱 LeafGuard AI - Protéger les cultures avec un monitoring intelligent",
                "footer_subtext": "Détection avancée des maladies végétales alimentée par l'IA"
            },
            "de": {
                "app_title": "🌱 LeafGuard AI",
                "app_subtitle": "KI-gestützte Pflanzenkrankheitserkennung und -analyse",
                "app_description": "Fortschrittliche Pflanzengesundheitsdiagnostik für Landwirte und landwirtschaftliche Fachkräfte",
                "upload_title": "📤 Pflanzenbilder hochladen",
                "upload_description": "Laden Sie ein oder mehrere Blattbilder zur Krankheitsanalyse hoch. Unterstützte Formate: JPG, PNG, JPEG",
                "choose_files": "Dateien auswählen",
                "analysis_results": "🔍 Analyseergebnisse",
                "processing": "Verarbeitung",
                "analysis_complete": "✅ Analyse abgeschlossen für",
                "download_report": "📄 LeafGuard-Bericht herunterladen",
                "report_generated": "📊 Bericht mit Krankheitsklassifizierung und Schweregradanalyse generiert",
                "error_processing": "❌ Fehler bei der Verarbeitung",
                "all_processed": "🎉 Alle Bilder erfolgreich verarbeitet!",
                "about_title": "🚀 Über LeafGuard AI",
                "about_description": "LeafGuard AI verwendet fortschrittliches maschinelles Lernen für:",
                "features_title": "📋 Unterstützte Funktionen",
                "detect_diseases": "🔍 Pflanzenkrankheiten mit hoher Genauigkeit erkennen",
                "estimate_severity": "📊 Krankheitsschweregrade schätzen",
                "generate_heatmaps": "🗺️ Visuelle Heatmaps zur Analyse generieren",
                "create_reports": "📋 Detaillierte PDF-Berichte erstellen",
                "store_results": "💾 Ergebnisse für zukünftige Referenz speichern",
                "batch_upload": "Batch-Bildupload",
                "multiple_classification": "Multiple Krankheitsklassifizierung",
                "severity_estimation": "Schweregradschätzung",
                "grad_cam_heatmaps": "Grad-CAM Heatmaps",
                "pdf_reports": "PDF-Berichtsgenerierung",
                "database_storage": "Datenbankspeicherung",
                "footer_text": "🌱 LeafGuard AI - Schutz der Ernten durch intelligente Überwachung",
                "footer_subtext": "Fortschrittliche Pflanzenkrankheitserkennung mit KI"
            }
        }
        
        # Disease Information Translations
        disease_translations = {
            "en": {
                "bacterial_spot": {
                    "name": "Bacterial Spot",
                    "description": "A bacterial disease that causes dark, water-soaked lesions on leaves, stems, and fruits.",
                    "treatment": "Remove infected plants, apply copper-based bactericides, and improve air circulation."
                },
                "early_blight": {
                    "name": "Early Blight",
                    "description": "A fungal disease characterized by dark brown spots with concentric rings on lower leaves.",
                    "treatment": "Apply fungicides, remove infected leaves, and maintain proper plant spacing."
                },
                "late_blight": {
                    "name": "Late Blight",
                    "description": "A devastating fungal disease that can rapidly destroy entire crops.",
                    "treatment": "Immediate fungicide application, remove infected plants, and improve drainage."
                },
                "healthy": {
                    "name": "Healthy",
                    "description": "The plant shows no signs of disease and appears to be in good health.",
                    "treatment": "Continue regular monitoring and maintain good agricultural practices."
                }
            },
            "es": {
                "bacterial_spot": {
                    "name": "Mancha Bacteriana",
                    "description": "Una enfermedad bacteriana que causa lesiones oscuras y empapadas de agua en hojas, tallos y frutos.",
                    "treatment": "Eliminar plantas infectadas, aplicar bactericidas a base de cobre y mejorar la circulación del aire."
                },
                "early_blight": {
                    "name": "Tizón Temprano",
                    "description": "Una enfermedad fúngica caracterizada por manchas marrón oscuro con anillos concéntricos en las hojas inferiores.",
                    "treatment": "Aplicar fungicidas, eliminar hojas infectadas y mantener el espaciado adecuado entre plantas."
                },
                "late_blight": {
                    "name": "Tizón Tardío",
                    "description": "Una devastadora enfermedad fúngica que puede destruir rápidamente cultivos enteros.",
                    "treatment": "Aplicación inmediata de fungicidas, eliminar plantas infectadas y mejorar el drenaje."
                },
                "healthy": {
                    "name": "Saludable",
                    "description": "La planta no muestra signos de enfermedad y parece estar en buen estado de salud.",
                    "treatment": "Continuar con el monitoreo regular y mantener buenas prácticas agrícolas."
                }
            },
            "fr": {
                "bacterial_spot": {
                    "name": "Tache Bactérienne",
                    "description": "Une maladie bactérienne qui cause des lésions sombres et imbibées d'eau sur les feuilles, tiges et fruits.",
                    "treatment": "Supprimer les plantes infectées, appliquer des bactéricides à base de cuivre et améliorer la circulation d'air."
                },
                "early_blight": {
                    "name": "Mildiou Précoce",
                    "description": "Une maladie fongique caractérisée par des taches brun foncé avec des anneaux concentriques sur les feuilles inférieures.",
                    "treatment": "Appliquer des fongicides, supprimer les feuilles infectées et maintenir un espacement approprié des plantes."
                },
                "late_blight": {
                    "name": "Mildiou Tardif",
                    "description": "Une maladie fongique dévastatrice qui peut rapidement détruire des cultures entières.",
                    "treatment": "Application immédiate de fongicides, supprimer les plantes infectées et améliorer le drainage."
                },
                "healthy": {
                    "name": "Sain",
                    "description": "La plante ne présente aucun signe de maladie et semble être en bonne santé.",
                    "treatment": "Continuer la surveillance régulière et maintenir de bonnes pratiques agricoles."
                }
            },
            "de": {
                "bacterial_spot": {
                    "name": "Bakterienfleck",
                    "description": "Eine bakterielle Krankheit, die dunkle, wassergetränkte Läsionen an Blättern, Stängeln und Früchten verursacht.",
                    "treatment": "Infizierte Pflanzen entfernen, kupferbasierte Bakterizide anwenden und Luftzirkulation verbessern."
                },
                "early_blight": {
                    "name": "Früher Blattfleck",
                    "description": "Eine Pilzkrankheit, die durch dunkelbraune Flecken mit konzentrischen Ringen auf unteren Blättern gekennzeichnet ist.",
                    "treatment": "Fungizide anwenden, infizierte Blätter entfernen und angemessenen Pflanzenabstand einhalten."
                },
                "late_blight": {
                    "name": "Später Blattfleck",
                    "description": "Eine verheerende Pilzkrankheit, die schnell ganze Ernten zerstören kann.",
                    "treatment": "Sofortige Fungizidanwendung, infizierte Pflanzen entfernen und Drainage verbessern."
                },
                "healthy": {
                    "name": "Gesund",
                    "description": "Die Pflanze zeigt keine Krankheitsanzeichen und scheint in guter Gesundheit zu sein.",
                    "treatment": "Regelmäßige Überwachung fortsetzen und gute landwirtschaftliche Praktiken beibehalten."
                }
            }
        }
        
        # PDF Report Translations
        report_translations = {
            "en": {
                "report_title": "Plant Disease Detection Report",
                "analysis_results": "ANALYSIS RESULTS",
                "disease_detected": "Disease Detected",
                "severity_level": "Severity Level",
                "confidence": "Confidence",
                "disease_information": "DISEASE INFORMATION",
                "description": "Description",
                "treatment_advice": "Treatment Advice",
                "visual_analysis": "VISUAL ANALYSIS",
                "original_image": "Original Image",
                "ai_heatmap": "AI Heatmap Analysis",
                "images_not_available": "[Images not available]",
                "footer_text": "🌱 LeafGuard AI - AI-Powered Plant Disease Detection",
                "footer_subtext": "Protecting crops with intelligent monitoring"
            },
            "es": {
                "report_title": "Reporte de Detección de Enfermedades Vegetales",
                "analysis_results": "RESULTADOS DEL ANÁLISIS",
                "disease_detected": "Enfermedad Detectada",
                "severity_level": "Nivel de Severidad",
                "confidence": "Confianza",
                "disease_information": "INFORMACIÓN DE LA ENFERMEDAD",
                "description": "Descripción",
                "treatment_advice": "Consejos de Tratamiento",
                "visual_analysis": "ANÁLISIS VISUAL",
                "original_image": "Imagen Original",
                "ai_heatmap": "Análisis de Mapa de Calor IA",
                "images_not_available": "[Imágenes no disponibles]",
                "footer_text": "🌱 LeafGuard AI - Detección de Enfermedades Vegetales con IA",
                "footer_subtext": "Protegiendo cultivos con monitoreo inteligente"
            },
            "fr": {
                "report_title": "Rapport de Détection des Maladies Végétales",
                "analysis_results": "RÉSULTATS DE L'ANALYSE",
                "disease_detected": "Maladie Détectée",
                "severity_level": "Niveau de Sévérité",
                "confidence": "Confiance",
                "disease_information": "INFORMATIONS SUR LA MALADIE",
                "description": "Description",
                "treatment_advice": "Conseils de Traitement",
                "visual_analysis": "ANALYSE VISUELLE",
                "original_image": "Image Originale",
                "ai_heatmap": "Analyse de Carte de Chaleur IA",
                "images_not_available": "[Images non disponibles]",
                "footer_text": "🌱 LeafGuard AI - Détection des Maladies Végétales par IA",
                "footer_subtext": "Protéger les cultures avec un monitoring intelligent"
            },
            "de": {
                "report_title": "Pflanzenkrankheitserkennungsbericht",
                "analysis_results": "ANALYSEERGEBNISSE",
                "disease_detected": "Erkannte Krankheit",
                "severity_level": "Schweregrad",
                "confidence": "Vertrauen",
                "disease_information": "KRANKHEITSINFORMATIONEN",
                "description": "Beschreibung",
                "treatment_advice": "Behandlungsempfehlungen",
                "visual_analysis": "VISUELLE ANALYSE",
                "original_image": "Originalbild",
                "ai_heatmap": "KI-Heatmap-Analyse",
                "images_not_available": "[Bilder nicht verfügbar]",
                "footer_text": "🌱 LeafGuard AI - KI-gestützte Pflanzenkrankheitserkennung",
                "footer_subtext": "Schutz der Ernten durch intelligente Überwachung"
            }
        }
        
        # Combine all translations
        for lang_code in self.supported_languages:
            translations[lang_code] = {
                "ui": ui_translations.get(lang_code, ui_translations["en"]),
                "diseases": disease_translations.get(lang_code, disease_translations["en"]),
                "reports": report_translations.get(lang_code, report_translations["en"])
            }
        
        return translations
    
    def get_text(self, key: str, language: str = "en", section: str = "ui") -> str:
        """Get translated text for a given key and language"""
        try:
            return self.translations[language][section][key]
        except KeyError:
            # Fallback to English
            try:
                return self.translations["en"][section][key]
            except KeyError:
                return key
    
    def get_disease_info(self, disease_key: str, language: str = "en") -> Dict:
        """Get disease information in specified language"""
        try:
            return self.translations[language]["diseases"][disease_key]
        except KeyError:
            # Fallback to English
            return self.translations["en"]["diseases"].get(disease_key, {
                "name": disease_key,
                "description": "No description available.",
                "treatment": "No treatment advice available."
            })
    
    def get_report_text(self, key: str, language: str = "en") -> str:
        """Get report text in specified language"""
        return self.get_text(key, language, "reports")
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported"""
        return language in self.supported_languages
    
    def get_language_name(self, language_code: str) -> str:
        """Get language name from language code"""
        return self.supported_languages.get(language_code, language_code)

# Global language manager instance
language_manager = LanguageManager() 