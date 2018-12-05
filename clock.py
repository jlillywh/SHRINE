import datetime

class Clock:
    def __init__(self, start_date=datetime.datetime.today(), duration = 100):
        self.start_date = start_date
        self.duration = duration
        self.end_date = start_date + duration

"""

require 'date'
class Clock
  attr_reader :current_date, :start_date, :end_date, :duration

  #Set up the clock initially
  # @param start_date [Date]
  # @param duration [int]
  def initialize(start_date=Date.today, duration=100)
    @start_date = start_date
    @duration = duration
    @current_date = @start_date
    @end_date = @start_date + @duration
  end

  #Increment the clock by 1 time step
  def increment
    @current_date += 1
  end

  # Set the start date, which resets the clock
  # @param new_date [Date]
  # @return [nil]
  def set_start_date(new_date)
    @start_date = new_date
    @current_date = @start_date
    @end_date = @start_date + duration
  end

  # Set the duration, which causes the end_date to update
  # @param duration [int]
  # @return [nil]
  def set_duration new_duration
    @duration = new_duration
    @end_date = @start_date + @duration
  end

  #Print the summary of the clock properties
  def to_s
    object_summary = %{Summary of the Clock: \
    \nClock start: #{self.start_date} \
    \nClock end: #{self.end_date}\n\n}
    return object_summary
  end
end



"""