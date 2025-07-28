"""
Outils de planification et priorisation pour l'ADK (Agent Development Kit)
Permet aux agents de planifier et prioriser les tâches de maintenance
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from adk.api.tool_manager import tool

# Critères de priorisation
PRIORITY_CRITERIA = {
    "safety": {
        "weight": 10,
        "description": "Impact sur la sécurité",
        "levels": {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 1
        }
    },
    "production": {
        "weight": 8,
        "description": "Impact sur la production",
        "levels": {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 1
        }
    },
    "equipment_criticality": {
        "weight": 7,
        "description": "Criticité de l'équipement",
        "levels": {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 1
        }
    },
    "urgency": {
        "weight": 6,
        "description": "Urgence de l'intervention",
        "levels": {
            "immediate": 10,
            "urgent": 8,
            "high": 6,
            "medium": 4,
            "low": 2
        }
    },
    "resource_availability": {
        "weight": 5,
        "description": "Disponibilité des ressources",
        "levels": {
            "available": 10,
            "limited": 6,
            "scarce": 3,
            "unavailable": 1
        }
    }
}

@tool
async def prioritize_maintenance_tasks(
    tasks: List[Dict[str, Any]],
    priority_factors: Optional[Dict[str, str]] = None
) -> str:
    """
    Priorise les tâches de maintenance selon des critères métier.
    Utilisez cet outil pour déterminer l'ordre d'exécution optimal des tâches.
    
    Args:
        tasks: Liste des tâches à prioriser
        priority_factors: Facteurs de priorité personnalisés (optionnel)
    
    Returns:
        Liste des tâches triées par priorité avec scores
    """
    try:
        if not tasks:
            return "❌ Aucune tâche à prioriser"
        
        # Utilisation des critères par défaut si aucun facteur personnalisé
        if not priority_factors:
            priority_factors = {
                "safety": "medium",
                "production": "medium", 
                "equipment_criticality": "medium",
                "urgency": "medium",
                "resource_availability": "available"
            }
        
        prioritized_tasks = []
        
        for task in tasks:
            # Calcul du score de priorité
            priority_score = 0
            max_possible_score = 0
            
            for criterion, weight_info in PRIORITY_CRITERIA.items():
                weight = weight_info["weight"]
                max_possible_score += weight * 10  # Score max par critère
                
                # Récupération du niveau pour ce critère
                level = priority_factors.get(criterion, "medium")
                level_score = weight_info["levels"].get(level, 5)
                
                # Ajustements spécifiques selon le type de tâche
                if criterion == "safety" and task.get("safety_impact"):
                    level_score = weight_info["levels"].get(task["safety_impact"], level_score)
                
                if criterion == "production" and task.get("production_impact"):
                    level_score = weight_info["levels"].get(task["production_impact"], level_score)
                
                if criterion == "equipment_criticality" and task.get("equipment_criticality"):
                    level_score = weight_info["levels"].get(task["equipment_criticality"], level_score)
                
                if criterion == "urgency" and task.get("urgency"):
                    level_score = weight_info["levels"].get(task["urgency"], level_score)
                
                priority_score += weight * level_score
            
            # Calcul du pourcentage de priorité
            priority_percentage = (priority_score / max_possible_score) * 100
            
            # Détermination du niveau de priorité
            if priority_percentage >= 80:
                priority_level = "CRITIQUE"
            elif priority_percentage >= 60:
                priority_level = "ÉLEVÉE"
            elif priority_percentage >= 40:
                priority_level = "MOYENNE"
            else:
                priority_level = "FAIBLE"
            
            prioritized_task = {
                **task,
                "priority_score": priority_score,
                "priority_percentage": round(priority_percentage, 1),
                "priority_level": priority_level
            }
            
            prioritized_tasks.append(prioritized_task)
        
        # Tri par score de priorité décroissant
        prioritized_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Formatage de la réponse
        result = f"📊 PRIORISATION DES TÂCHES ({len(tasks)} tâches analysées)\n\n"
        
        for i, task in enumerate(prioritized_tasks, 1):
            result += f"{i}. {task.get('description', 'Tâche sans description')}\n"
            result += f"   🏭 Équipement: {task.get('equipment_id', 'N/A')}\n"
            result += f"   ⚡ Priorité: {task['priority_level']} ({task['priority_percentage']}%)\n"
            result += f"   📅 Date prévue: {task.get('planned_date', 'N/A')}\n"
            result += f"   ⏱️ Durée estimée: {task.get('estimated_duration', 'N/A')}\n\n"
        
        # Sauvegarde des résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prioritization_results_{timestamp}.json"
        filepath = f"planning/{filename}"
        
        os.makedirs("planning", exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "prioritized_tasks": prioritized_tasks,
                "priority_factors": priority_factors,
                "generated_at": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        result += f"💾 Résultats sauvegardés dans: {filepath}"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de la priorisation: {str(e)}"

@tool
async def create_maintenance_schedule(
    tasks: List[Dict[str, Any]],
    available_resources: List[Dict[str, Any]],
    schedule_period: str = "7",
    work_hours: Dict[str, int] = None
) -> str:
    """
    Crée un planning de maintenance optimisé.
    Utilisez cet outil pour planifier les interventions selon les ressources disponibles.
    
    Args:
        tasks: Tâches de maintenance à planifier
        available_resources: Ressources disponibles (techniciens, équipements)
        schedule_period: Période de planification en jours
        work_hours: Heures de travail par jour (optionnel)
    
    Returns:
        Planning détaillé avec affectation des ressources
    """
    try:
        if not tasks:
            return "❌ Aucune tâche à planifier"
        
        if not available_resources:
            return "❌ Aucune ressource disponible"
        
        # Configuration des heures de travail par défaut
        if not work_hours:
            work_hours = {
                "start": 8,
                "end": 17,
                "break_duration": 60  # minutes
            }
        
        # Calcul des heures de travail effectives par jour
        work_hours_per_day = work_hours["end"] - work_hours["start"] - (work_hours["break_duration"] / 60)
        
        # Tri des tâches par priorité
        prioritized_tasks = []
        for task in tasks:
            # Calcul d'un score de priorité simple
            priority_score = 0
            if task.get("urgency") == "urgent":
                priority_score += 10
            if task.get("equipment_criticality") == "critical":
                priority_score += 8
            if task.get("safety_impact") == "high":
                priority_score += 6
            
            prioritized_tasks.append({
                **task,
                "priority_score": priority_score
            })
        
        prioritized_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Création du planning
        schedule = {
            "period": f"{schedule_period} jours",
            "work_hours": work_hours,
            "total_work_hours": work_hours_per_day * int(schedule_period),
            "scheduled_tasks": [],
            "resource_assignments": {},
            "daily_schedules": {}
        }
        
        current_date = datetime.now()
        current_hour = work_hours["start"]
        current_day = 0
        
        for task in prioritized_tasks:
            # Estimation de la durée (en heures)
            estimated_duration = task.get("estimated_duration_hours", 2)
            
            # Vérification si la tâche peut être planifiée aujourd'hui
            if current_hour + estimated_duration > work_hours["end"]:
                # Passer au jour suivant
                current_day += 1
                current_hour = work_hours["start"]
                
                if current_day >= int(schedule_period):
                    break
            
            # Recherche d'une ressource disponible
            assigned_resource = None
            for resource in available_resources:
                if resource.get("available", True) and resource.get("skills", []):
                    # Vérification des compétences requises
                    required_skills = task.get("required_skills", [])
                    if not required_skills or any(skill in resource.get("skills", []) for skill in required_skills):
                        assigned_resource = resource
                        break
            
            if assigned_resource:
                # Planification de la tâche
                task_schedule = {
                    "task_id": task.get("id"),
                    "description": task.get("description"),
                    "equipment_id": task.get("equipment_id"),
                    "priority_level": task.get("priority_level", "MOYENNE"),
                    "scheduled_date": (current_date + timedelta(days=current_day)).strftime("%Y-%m-%d"),
                    "start_time": f"{current_hour:02d}:00",
                    "end_time": f"{current_hour + estimated_duration:02d}:00",
                    "duration_hours": estimated_duration,
                    "assigned_resource": assigned_resource.get("name", "N/A"),
                    "resource_id": assigned_resource.get("id")
                }
                
                schedule["scheduled_tasks"].append(task_schedule)
                
                # Mise à jour de l'heure courante
                current_hour += estimated_duration
                
                # Ajout d'un buffer entre les tâches
                current_hour += 0.5
                
                # Mise à jour des affectations de ressources
                if assigned_resource.get("id") not in schedule["resource_assignments"]:
                    schedule["resource_assignments"][assigned_resource.get("id")] = []
                schedule["resource_assignments"][assigned_resource.get("id")].append(task_schedule)
        
        # Création des plannings quotidiens
        for day in range(int(schedule_period)):
            date = (current_date + timedelta(days=day)).strftime("%Y-%m-%d")
            day_tasks = [t for t in schedule["scheduled_tasks"] if t["scheduled_date"] == date]
            schedule["daily_schedules"][date] = day_tasks
        
        # Formatage de la réponse
        result = f"📅 PLANNING DE MAINTENANCE ({schedule_period} jours)\n\n"
        result += f"⏰ Heures de travail: {work_hours['start']}h-{work_hours['end']}h\n"
        result += f"👥 Ressources disponibles: {len(available_resources)}\n"
        result += f"📋 Tâches planifiées: {len(schedule['scheduled_tasks'])}\n\n"
        
        # Affichage par jour
        for date, day_tasks in schedule["daily_schedules"].items():
            if day_tasks:
                result += f"📆 {date}:\n"
                for task in day_tasks:
                    result += f"   • {task['start_time']}-{task['end_time']}: {task['description']}\n"
                    result += f"     🏭 {task['equipment_id']} | 👷 {task['assigned_resource']} | ⚡ {task['priority_level']}\n"
                result += "\n"
        
        # Sauvegarde du planning
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"maintenance_schedule_{timestamp}.json"
        filepath = f"planning/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
        
        result += f"💾 Planning sauvegardé dans: {filepath}"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de la création du planning: {str(e)}"

@tool
async def optimize_resource_allocation(
    tasks: List[Dict[str, Any]],
    resources: List[Dict[str, Any]],
    optimization_criteria: str = "efficiency"
) -> str:
    """
    Optimise l'allocation des ressources pour les tâches de maintenance.
    Utilisez cet outil pour maximiser l'efficacité de l'équipe de maintenance.
    
    Args:
        tasks: Tâches à exécuter
        resources: Ressources disponibles
        optimization_criteria: Critère d'optimisation ('efficiency', 'cost', 'time')
    
    Returns:
        Allocation optimisée des ressources
    """
    try:
        if not tasks or not resources:
            return "❌ Tâches ou ressources manquantes"
        
        # Analyse des compétences requises
        required_skills = set()
        for task in tasks:
            task_skills = task.get("required_skills", [])
            required_skills.update(task_skills)
        
        # Analyse des compétences disponibles
        available_skills = {}
        for resource in resources:
            resource_skills = resource.get("skills", [])
            for skill in resource_skills:
                if skill not in available_skills:
                    available_skills[skill] = []
                available_skills[skill].append(resource)
        
        # Vérification de la couverture des compétences
        missing_skills = required_skills - set(available_skills.keys())
        if missing_skills:
            return f"❌ Compétences manquantes: {', '.join(missing_skills)}"
        
        # Optimisation selon le critère
        if optimization_criteria == "efficiency":
            allocation = await _optimize_for_efficiency(tasks, resources)
        elif optimization_criteria == "cost":
            allocation = await _optimize_for_cost(tasks, resources)
        elif optimization_criteria == "time":
            allocation = await _optimize_for_time(tasks, resources)
        else:
            return f"❌ Critère d'optimisation non supporté: {optimization_criteria}"
        
        # Formatage de la réponse
        result = f"🎯 OPTIMISATION DES RESSOURCES ({optimization_criteria.upper()})\n\n"
        
        for task_allocation in allocation:
            task = task_allocation["task"]
            resource = task_allocation["resource"]
            score = task_allocation.get("match_score", 0)
            
            result += f"📋 {task.get('description', 'Tâche sans description')}\n"
            result += f"   🏭 Équipement: {task.get('equipment_id', 'N/A')}\n"
            result += f"   👷 Ressource assignée: {resource.get('name', 'N/A')}\n"
            result += f"   🎯 Score de compatibilité: {score:.1f}%\n"
            result += f"   🔧 Compétences requises: {', '.join(task.get('required_skills', []))}\n"
            result += f"   ✅ Compétences disponibles: {', '.join(resource.get('skills', []))}\n\n"
        
        # Statistiques d'optimisation
        total_tasks = len(tasks)
        total_resources = len(resources)
        avg_score = sum(a.get("match_score", 0) for a in allocation) / len(allocation) if allocation else 0
        
        result += f"📊 STATISTIQUES:\n"
        result += f"   • Tâches optimisées: {total_tasks}\n"
        result += f"   • Ressources utilisées: {total_resources}\n"
        result += f"   • Score moyen de compatibilité: {avg_score:.1f}%\n"
        
        # Sauvegarde de l'allocation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resource_allocation_{optimization_criteria}_{timestamp}.json"
        filepath = f"planning/{filename}"
        
        os.makedirs("planning", exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "allocation": allocation,
                "optimization_criteria": optimization_criteria,
                "statistics": {
                    "total_tasks": total_tasks,
                    "total_resources": total_resources,
                    "average_match_score": avg_score
                },
                "generated_at": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        result += f"💾 Allocation sauvegardée dans: {filepath}"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de l'optimisation: {str(e)}"

async def _optimize_for_efficiency(tasks: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimise pour l'efficacité (meilleure correspondance compétences/tâches)"""
    allocation = []
    used_resources = set()
    
    for task in tasks:
        best_resource = None
        best_score = 0
        
        for resource in resources:
            if resource.get("id") in used_resources:
                continue
            
            # Calcul du score de compatibilité
            required_skills = set(task.get("required_skills", []))
            available_skills = set(resource.get("skills", []))
            
            if required_skills:
                match_score = len(required_skills.intersection(available_skills)) / len(required_skills) * 100
            else:
                match_score = 50  # Score par défaut si pas de compétences requises
            
            # Bonus pour l'expérience
            experience_bonus = min(resource.get("experience_years", 0) * 5, 20)
            match_score += experience_bonus
            
            if match_score > best_score:
                best_score = match_score
                best_resource = resource
        
        if best_resource:
            allocation.append({
                "task": task,
                "resource": best_resource,
                "match_score": best_score
            })
            used_resources.add(best_resource.get("id"))
    
    return allocation

async def _optimize_for_cost(tasks: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimise pour le coût (ressources les moins chères)"""
    allocation = []
    used_resources = set()
    
    # Tri des ressources par coût horaire
    sorted_resources = sorted(resources, key=lambda r: r.get("hourly_rate", 0))
    
    for task in tasks:
        for resource in sorted_resources:
            if resource.get("id") in used_resources:
                continue
            
            # Vérification des compétences minimales
            required_skills = set(task.get("required_skills", []))
            available_skills = set(resource.get("skills", []))
            
            if not required_skills or required_skills.intersection(available_skills):
                allocation.append({
                    "task": task,
                    "resource": resource,
                    "match_score": 100 - resource.get("hourly_rate", 0)  # Score inversé au coût
                })
                used_resources.add(resource.get("id"))
                break
    
    return allocation

async def _optimize_for_time(tasks: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimise pour le temps (ressources les plus rapides)"""
    allocation = []
    used_resources = set()
    
    # Tri des ressources par productivité
    sorted_resources = sorted(resources, key=lambda r: r.get("productivity_score", 0), reverse=True)
    
    for task in tasks:
        for resource in sorted_resources:
            if resource.get("id") in used_resources:
                continue
            
            # Vérification des compétences
            required_skills = set(task.get("required_skills", []))
            available_skills = set(resource.get("skills", []))
            
            if not required_skills or required_skills.intersection(available_skills):
                allocation.append({
                    "task": task,
                    "resource": resource,
                    "match_score": resource.get("productivity_score", 50)
                })
                used_resources.add(resource.get("id"))
                break
    
    return allocation

@tool
async def analyze_maintenance_trends(
    historical_data: List[Dict[str, Any]],
    analysis_period: str = "30",
    trend_type: str = "equipment_failures"
) -> str:
    """
    Analyse les tendances de maintenance pour améliorer la planification.
    Utilisez cet outil pour identifier les patterns et optimiser la maintenance préventive.
    
    Args:
        historical_data: Données historiques de maintenance
        analysis_period: Période d'analyse en jours
        trend_type: Type d'analyse ('equipment_failures', 'downtime', 'costs')
    
    Returns:
        Analyse des tendances avec recommandations
    """
    try:
        if not historical_data:
            return "❌ Aucune donnée historique disponible"
        
        # Filtrage par période
        cutoff_date = datetime.now() - timedelta(days=int(analysis_period))
        filtered_data = [
            record for record in historical_data
            if datetime.fromisoformat(record.get("date", "2020-01-01")) >= cutoff_date
        ]
        
        if not filtered_data:
            return f"❌ Aucune donnée dans les {analysis_period} derniers jours"
        
        # Analyse selon le type
        if trend_type == "equipment_failures":
            analysis = await _analyze_equipment_failures(filtered_data)
        elif trend_type == "downtime":
            analysis = await _analyze_downtime_trends(filtered_data)
        elif trend_type == "costs":
            analysis = await _analyze_cost_trends(filtered_data)
        else:
            return f"❌ Type d'analyse non supporté: {trend_type}"
        
        # Formatage de la réponse
        result = f"📈 ANALYSE DES TENDANCES ({trend_type.replace('_', ' ').title()})\n\n"
        result += f"📊 Période analysée: {analysis_period} derniers jours\n"
        result += f"📋 Enregistrements analysés: {len(filtered_data)}\n\n"
        
        result += analysis["summary"]
        result += "\n\n🎯 RECOMMANDATIONS:\n"
        result += analysis["recommendations"]
        
        # Sauvegarde de l'analyse
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trend_analysis_{trend_type}_{timestamp}.json"
        filepath = f"planning/{filename}"
        
        os.makedirs("planning", exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "analysis_type": trend_type,
                "period_days": analysis_period,
                "records_analyzed": len(filtered_data),
                "analysis_results": analysis,
                "generated_at": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        result += f"\n💾 Analyse sauvegardée dans: {filepath}"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de l'analyse des tendances: {str(e)}"

async def _analyze_equipment_failures(data: List[Dict[str, Any]]) -> Dict[str, str]:
    """Analyse les tendances de défaillances d'équipements"""
    # Groupement par équipement
    equipment_failures = {}
    for record in data:
        equipment_id = record.get("equipment_id", "Unknown")
        if equipment_id not in equipment_failures:
            equipment_failures[equipment_id] = []
        equipment_failures[equipment_id].append(record)
    
    # Calcul des statistiques
    failure_stats = []
    for equipment_id, failures in equipment_failures.items():
        failure_count = len(failures)
        avg_downtime = sum(f.get("downtime_hours", 0) for f in failures) / failure_count if failure_count > 0 else 0
        failure_stats.append({
            "equipment_id": equipment_id,
            "failure_count": failure_count,
            "avg_downtime": avg_downtime,
            "total_downtime": sum(f.get("downtime_hours", 0) for f in failures)
        })
    
    # Tri par nombre de défaillances
    failure_stats.sort(key=lambda x: x["failure_count"], reverse=True)
    
    summary = "🏭 ÉQUIPEMENTS LES PLUS DÉFAILLANTS:\n"
    for i, stat in enumerate(failure_stats[:5], 1):
        summary += f"   {i}. {stat['equipment_id']}: {stat['failure_count']} défaillances\n"
        summary += f"      ⏱️ Temps d'arrêt moyen: {stat['avg_downtime']:.1f}h\n"
    
    recommendations = "• Planifier une maintenance préventive renforcée pour les équipements critiques\n"
    recommendations += "• Analyser les causes racines des défaillances récurrentes\n"
    recommendations += "• Mettre en place un monitoring prédictif pour les équipements à risque\n"
    recommendations += "• Former les équipes sur les équipements problématiques\n"
    
    return {
        "summary": summary,
        "recommendations": recommendations
    }

async def _analyze_downtime_trends(data: List[Dict[str, Any]]) -> Dict[str, str]:
    """Analyse les tendances de temps d'arrêt"""
    # Calcul du temps d'arrêt total par jour
    daily_downtime = {}
    for record in data:
        date = record.get("date", "2020-01-01")[:10]  # YYYY-MM-DD
        downtime = record.get("downtime_hours", 0)
        if date not in daily_downtime:
            daily_downtime[date] = 0
        daily_downtime[date] += downtime
    
    total_downtime = sum(daily_downtime.values())
    avg_daily_downtime = total_downtime / len(daily_downtime) if daily_downtime else 0
    
    summary = f"⏱️ ANALYSE DES TEMPS D'ARRÊT:\n"
    summary += f"   • Temps d'arrêt total: {total_downtime:.1f} heures\n"
    summary += f"   • Temps d'arrêt moyen par jour: {avg_daily_downtime:.1f} heures\n"
    summary += f"   • Jours avec arrêts: {len(daily_downtime)} sur {len(set(r.get('date', '')[:10] for r in data))}\n"
    
    recommendations = "• Optimiser les procédures de maintenance pour réduire les temps d'arrêt\n"
    recommendations += "• Planifier les interventions pendant les périodes de faible activité\n"
    recommendations += "• Améliorer la coordination entre les équipes de maintenance\n"
    recommendations += "• Investir dans des équipements de diagnostic avancés\n"
    
    return {
        "summary": summary,
        "recommendations": recommendations
    }

async def _analyze_cost_trends(data: List[Dict[str, Any]]) -> Dict[str, str]:
    """Analyse les tendances de coûts"""
    # Calcul des coûts par type de maintenance
    cost_by_type = {}
    total_cost = 0
    
    for record in data:
        maintenance_type = record.get("maintenance_type", "Unknown")
        cost = record.get("cost", 0)
        total_cost += cost
        
        if maintenance_type not in cost_by_type:
            cost_by_type[maintenance_type] = 0
        cost_by_type[maintenance_type] += cost
    
    summary = f"💰 ANALYSE DES COÛTS:\n"
    summary += f"   • Coût total: {total_cost:.2f} €\n"
    summary += f"   • Coût moyen par intervention: {total_cost/len(data):.2f} €\n\n"
    
    summary += "📊 RÉPARTITION PAR TYPE:\n"
    for maint_type, cost in sorted(cost_by_type.items(), key=lambda x: x[1], reverse=True):
        percentage = (cost / total_cost * 100) if total_cost > 0 else 0
        summary += f"   • {maint_type}: {cost:.2f} € ({percentage:.1f}%)\n"
    
    recommendations = "• Optimiser les coûts en privilégiant la maintenance préventive\n"
    recommendations += "• Négocier les prix avec les fournisseurs de pièces détachées\n"
    recommendations += "• Former les équipes pour réduire les interventions externes\n"
    recommendations += "• Analyser le ROI des investissements en équipements\n"
    
    return {
        "summary": summary,
        "recommendations": recommendations
    } 