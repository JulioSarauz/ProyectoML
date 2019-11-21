gl_speech <- function(audio_source,
                      encoding = c("LINEAR16","FLAC","MULAW","AMR",
                                   "AMR_WB","OGG_OPUS","SPEEX_WITH_HEADER_BYTE"),
                      sampleRateHertz = NULL,
                      languageCode = "en-US",
                      maxAlternatives = 1L,
                      profanityFilter = FALSE,
                      speechContexts = NULL,
                      asynch = FALSE,
                      customConfig = NULL){
  
  if(is.null(sampleRateHertz)){
    my_message("Setting sampleRateHertz = 16000L")
    sampleRateHertz <- 16000L
  }
  assert_that(is.string(audio_source),
              is.string(languageCode),
              is.numeric(maxAlternatives),
              is.scalar(sampleRateHertz),
              is.logical(profanityFilter))
  
  encoding <- match.arg(encoding)
  
  if(is.gcs(audio_source)){
    recognitionAudio <- list(
      uri = audio_source
    )
  } else {
    assert_that(is.readable(audio_source))
    
    recognitionAudio <- list(
      content = base64encode(audio_source)
    )
  }
  
  if(!is.null(customConfig)){
    assert_that(is.list(customConfig))
    config <- customConfig
    
    # config has to include languageCode, if not present use argument
    if(is.null(config$languageCode)){
      config$languageCode <- languageCode
    }
    
  } else {
    config <- list(
      encoding = encoding,
      sampleRateHertz = sampleRateHertz,
      languageCode = languageCode,
      maxAlternatives = maxAlternatives,
      profanityFilter = profanityFilter,
      speechContexts = speechContexts,
      enableWordTimeOffsets = TRUE
    )
  }
  
  body <- list(
    config = config,
    audio = recognitionAudio
  )
  
  # beta or production API endpoint
  endpoint <- sprintf("https://speech.googleapis.com/%s/speech:", get_version("speech"))
  
  ## asynch or normal call?
  if(asynch){
    call_api <- gar_api_generator(paste0(endpoint, "longrunningrecognize"),
                                  "POST",
                                  data_parse_function = parse_async)
    
  } else {
    
    call_api <- gar_api_generator(paste0(endpoint, "recognize"),
                                  "POST",
                                  data_parse_function = parse_speech)
  }
  
  call_api(the_body = body)
  
}

# parse normal speech call responses
parse_speech <- function(x){
  
  if(!is.null(x$totalBilledTime)){
    my_message("Speech transcription finished. Total billed time: ",
               x$totalBilledTime, level = 3)
  }
  
  transcript <-
    my_map_df(x$results$alternatives,
              ~ as_tibble(cbind(transcript = ifelse(!is.null(.x$transcript),
                                                    .x$transcript,NA),
                                confidence = ifelse(!is.null(.x$confidence),
                                                    .x$confidence,NA))))
  timings <- map(x$results$alternatives,
                 ~ .x$words[[1]])
  
  alts <- cbind(transcript,
                languageCode = as.character(x$results$languageCode),
                channelTag = if(!is.null(x$results$channelTag)) x$results$channelTag else NA,
                stringsAsFactors = FALSE)
  
  list(transcript = alts,
       timings = timings)
}

# parse asynchronous speech calls responses
parse_async <- function(x){
  
  if(is.null(x$done)){
    my_message("Speech transcription running")
    if(!is.null(x$metadata$startTime)){
      my_message("- started at ", x$metadata$startTime,
                 " - last update: ", x$metadata$lastUpdateTime,
                 level = 3)
    }
    return(structure(x, class = "gl_speech_op"))
  } else {
    my_message("Asynchronous transcription finished.", level = 3)
  }
  
  parse_speech(x$response)
  
}

#' pretty print of gl_speech_op
#' @export
#' @keywords internal
#' @noRd
print.gl_speech_op <- function(x, ...){
  cat("## Send to gl_speech_op() for status")
  cat("\n##", x$name)
}

# checks if gl_speech_op class
is.gl_speech_op <- function(x){
  inherits(x, "gl_speech_op")
}

#' Get a speech operation
#'
#' For asynchronous calls of audio over 60 seconds, this returns the finished job
#'
#' @param operation A speech operation object from \link{gl_speech} when \code{asynch = TRUE}
#'
#' @return If the operation is still running, another operation object.  If done, the result as per \link{gl_speech}
#'
#' @seealso \link{gl_speech}
#' @export
#' @import assertthat
#' @examples
#'
#' \dontrun{
#'
#' test_audio <- system.file("woman1_wb.wav", package = "googleLanguageR")
#'
#' ## make an asynchronous API request (mandatory for sound files over 60 seconds)
#' asynch <- gl_speech(test_audio, asynch = TRUE)
#'
#' ## Send to gl_speech_op() for status or finished result
#' gl_speech_op(asynch)
#'
#' }
#'
gl_speech_op <- function(operation = .Last.value){
  
  assert_that(
    is.gl_speech_op(operation)
  )
  
  call_api <- gar_api_generator(sprintf("https://speech.googleapis.com/v1/operations/%s", operation$name),
                                "GET",
                                data_parse_function = parse_async)
  call_api()
  
}
