# NVDA Coach - Progress Tracker
# Saves and loads lesson completion data for the current user.

import os
import json
import globalVars
from logHandler import log
from datetime import datetime


class ProgressTracker:
	"""Manages persistent storage of lesson progress."""

	def __init__(self):
		self._progressFile = os.path.join(
			globalVars.appArgs.configPath, "nvdaCoachProgress.json"
		)
		self._data = self._load()

	def _load(self):
		"""Load progress data from disk.

		This used to catch everything and return {}, which cannot tell "no
		file yet" from "the file is there and I could not read it". The next
		completed lesson then called _save() and wrote an almost empty file
		over the top, so one locked read - antivirus, a sync client, a
		roaming profile on a slow share - silently destroyed a student's
		entire course history and removed the evidence. Now an unreadable
		file is moved aside instead of overwritten.

		json.load also happily returns a list, a string or None for a file
		that is valid JSON but not an object. Every caller then does
		.get() on it and raises out of GlobalPlugin.__init__, which NVDA
		only logs - so the add-on would not load at all, with nothing spoken.
		"""
		if not os.path.exists(self._progressFile):
			return {}
		try:
			with open(self._progressFile, "r", encoding="utf-8") as f:
				data = json.load(f)
		except Exception as e:
			log.error(f"NVDA Coach: Could not read the progress file: {e}")
			self._preserveUnreadableFile()
			return {}
		if not isinstance(data, dict):
			log.error(
				"NVDA Coach: the progress file is valid JSON but not an object "
				f"(found {type(data).__name__}); keeping a copy and starting fresh"
			)
			self._preserveUnreadableFile()
			return {}
		# Drop anything that is not a category of lessons, rather than letting
		# it raise the first time something iterates it.
		return {k: v for k, v in data.items() if isinstance(v, dict)}

	def _preserveUnreadableFile(self):
		"""Move a progress file we could not read out of the way, not delete it.

		A student's progress is the only thing in this add-on that cannot be
		rebuilt, so a file we do not understand is renamed rather than
		overwritten. If that fails too, we leave it alone and accept losing
		the new progress instead of the old.
		"""
		spare = self._progressFile + ".unreadable"
		try:
			if os.path.exists(spare):
				os.remove(spare)
			os.replace(self._progressFile, spare)
			log.warning(f"NVDA Coach: kept the unreadable progress file at {spare}")
		except Exception as e:
			log.error(f"NVDA Coach: could not set the bad progress file aside: {e}")

	def _save(self):
		"""Write progress data to disk, atomically.

		The old version opened the real file with "w", which truncates before
		writing. Losing power, closing NVDA, or filling the disk part way
		through left a truncated file that the next load could not read. Now
		the new copy is written beside it and moved into place in one step, so
		the file on disk is always either the old progress or the new, never
		half of either.
		"""
		tmp = self._progressFile + ".tmp"
		try:
			with open(tmp, "w", encoding="utf-8") as f:
				json.dump(self._data, f, indent=2, ensure_ascii=False)
				f.flush()
				os.fsync(f.fileno())
			os.replace(tmp, self._progressFile)
		except Exception as e:
			log.error(f"NVDA Coach: Could not save progress file: {e}")
			try:
				if os.path.exists(tmp):
					os.remove(tmp)
			except Exception:
				pass

	def markLessonComplete(self, categoryId, lessonId, attempts, totalSteps):
		"""Record that a lesson was completed.

		Args:
			categoryId: The ID of the lesson category (e.g. "getting_started").
			lessonId: The ID of the specific lesson (e.g. "title_bar").
			attempts: Dict mapping step keys to attempt counts.
			totalSteps: Total number of steps in the lesson.
		"""
		if categoryId not in self._data:
			self._data[categoryId] = {}
		firstTryCount = sum(1 for v in attempts.values() if v == 1)
		self._data[categoryId][lessonId] = {
			"completed": True,
			"completedDate": datetime.now().isoformat(),
			"attempts": attempts,
			"firstTryCount": firstTryCount,
			"totalSteps": totalSteps,
		}
		self._save()

	def isLessonComplete(self, categoryId, lessonId):
		"""Check whether a lesson has been completed before."""
		category = self._data.get(categoryId, {})
		lesson = category.get(lessonId, {})
		return isinstance(lesson, dict) and lesson.get("completed", False)

	def getLessonResult(self, categoryId, lessonId):
		"""Return the stored result for a lesson, or None."""
		category = self._data.get(categoryId, {})
		return category.get(lessonId, None)

	def getCategoryProgress(self, categoryId, totalLessons):
		"""Return (completed_count, total) for a category."""
		category = self._data.get(categoryId, {})
		completed = sum(
			1 for v in category.values()
			if isinstance(v, dict) and v.get("completed")
		)
		return completed, totalLessons

	def resetProgress(self):
		"""Clear all progress data."""
		self._data = {}
		self._save()
