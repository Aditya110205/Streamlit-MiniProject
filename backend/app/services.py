def analyze_pipeline(data):
    records = data.records_processed
    failed = data.failed_records

    # Prevent invalid business data
    if failed > records:
        raise ValueError(
            "Failed records cannot exceed processed records."
        )

    # Calculate success rate
    if records == 0:
        success_rate = 0
    else:
        success_rate = ((records - failed) / records) * 100

    # Start with perfect quality
    quality_score = 100

    # Penalize null values
    quality_score -= data.null_percentage * 0.5

    # Penalize duplicates
    quality_score -= data.duplicate_percentage * 0.3

    # Penalize failed records
    quality_score -= (100 - success_rate) * 0.2

    # Keep score between 0 and 100
    quality_score = max(
        0,
        min(100, quality_score)
    )

    # Determine pipeline status
    if success_rate >= 99 and quality_score >= 90:
        status = "Healthy"

    elif success_rate >= 95 and quality_score >= 75:
        status = "Warning"

    else:
        status = "Critical"

    # Recommendations
    recommendations = []

    if data.null_percentage > 5:
        recommendations.append(
            "Investigate high null-value percentage."
        )

    if data.duplicate_percentage > 3:
        recommendations.append(
            "Check source data for duplicate records."
        )

    if success_rate < 95:
        recommendations.append(
            "Investigate failed records in the pipeline."
        )

    if data.processing_time > 300:
        recommendations.append(
            "Pipeline processing time is high."
        )

    if not recommendations:
        recommendations.append(
            "Pipeline is performing within expected limits."
        )

    return {
        "pipeline_name": data.pipeline_name,
        "status": status,
        "success_rate": round(success_rate, 2),
        "quality_score": round(quality_score, 2),
        "processing_time": data.processing_time,
        "recommendations": recommendations
    }