"""
Main entry point for the travel itinerary MVP system.
"""
import json
import logging
from datetime import datetime
from pathlib import Path

from travel_itinerary_mvp.graph.orchestrator import ItineraryOrchestrator
from travel_itinerary_mvp.config.settings import setup_logging, SYSTEM_SETTINGS
from travel_itinerary_mvp.persistence.repository import ItineraryRepository

def display_results(state, orchestrator):
    """Display the results of the itinerary generation process."""
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    
    summary = orchestrator.get_process_summary(state)
    
    print(f"🔸 Session ID: {summary['session_id']}")
    print(f"🔸 Iterations: {summary['iterations']}")
    print(f"🔸 Final Status: {summary['final_status']}")
    print(f"🔸 Approved: {'✅ Yes' if summary['approved'] else '❌ No'}")
    print(f"🔸 Final Score: {summary['final_score']:.1f}/10")
    
    if state.current_plan:
        print("\n📋 FINAL ITINERARY:")
        print(json.dumps(state.current_plan, indent=2, ensure_ascii=False))
    
    if state.critic_feedback and not state.approved:
        print("\n🔍 FINAL FEEDBACK:")
        feedback = state.critic_feedback
        print(f"Score: {feedback.get('score', 'N/A')}/10")
        if feedback.get('issues'):
            print("Issues:")
            for issue in feedback['issues']:
                print(f"  • {issue}")
        if feedback.get('improvements'):
            print("Suggested Improvements:")
            for improvement in feedback['improvements']:
                print(f"  • {improvement}")

def main():
    """Main function to run the travel itinerary system."""
    # Setup logging
    setup_logging(SYSTEM_SETTINGS)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Travel Itinerary MVP System")
    logger.info("=" * 60)
    
    # Initialize components
    orchestrator = ItineraryOrchestrator()
    repository = ItineraryRepository()
    
    print("\n🌍 Welcome to Travel Itinerary Generator!")
    print("Generate, review, and refine travel plans iteratively.\n")
    
    try:
        # Get user input
        print("Please describe your travel requirements:")
        print("(Example: '7 days trip to Japan with medium budget')")
        user_input = input("\n> ").strip()
        
        if not user_input:
            print("❌ No input provided. Exiting.")
            return
        
        print(f"\n🔄 Processing your request: '{user_input}'")
        print("This may take a few moments...\n")
        
        # Process the request
        final_state = orchestrator.process_request(
            user_input=user_input,
            max_iterations=SYSTEM_SETTINGS.MAX_ITERATIONS
        )
        
        # Display results
        display_results(final_state, orchestrator)
        
        # Save to repository
        if final_state.current_plan:
            save_result = repository.save_itinerary(
                final_state.current_plan,
                final_state.session_id,
                final_state.get_current_score(),
                final_state.approved
            )
            if save_result:
                print(f"\n💾 Itinerary saved with ID: {final_state.session_id}")
        
        logger.info("Application completed successfully")
        
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
        logger.info("Application cancelled by user")
    except Exception as e:
        error_msg = f"Application error: {str(e)}"
        print(f"\n❌ {error_msg}")
        logger.error(error_msg)
    
    print("\nThank you for using Travel Itinerary Generator! 🌟")

if __name__ == "__main__":
    main()
