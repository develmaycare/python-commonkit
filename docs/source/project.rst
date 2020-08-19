*******
Project
*******

Contributing
============

We welcome contributions to this and any of `our open source projects`_. There are a number of ways to participate and contribute. See :ref:`contact`.

.. _our open source projects: https://develmaycare.com/products/

Reporting Issues
----------------

Perhaps the easiest way to contribute is to submit an issue. If you have found a bug or error in the documentation, please submit a request. See :ref:`contact`.

.. important::
    Do **not** report security issues using the issue tracker. Instead, send an email to security@develmaycare.com with details on the issue you've discovered.

Submitting Feature Requests
---------------------------

Although we reserve the right to decline new features, we welcome all feature requests. See :ref:`contact`.

Testing and Quality Control
---------------------------

Testing involves using commonkit in real life or in development. Feel free to report any issues you find, or to improve the unit tests.

Pull Requests
-------------

Pull requests are welcome. Such requests should be associated with an issue. We may ignore pull requests that do not have a corresponding issue, so create an issue if one does not already exist.

Blogging
--------

You may help spread awareness of commonkit by writing blog posts. We are happy to link out to reviews and tutorials from our web site. `Let us know if you've created a blog post`_ that we can share. Be sure to include a link to the post.

You may also provide us with a guest post to be included on our blog.

.. _Let us know if you've created a blog post: https://develmaycare.com/contact/?product=commonkit

.. note::
    We reserve the right to proof and approve or decline all content posted on our web site.

Development
===========

Style Guide
-----------

commonkit follows `PEP8`_ and (where appropriate) the `Django style guide`_ and `JavaScript Standard Style`_.

.. _Django style guide: https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/
.. _JavaScript Standard Style: https://standardjs.com
.. _PEP8: https://www.python.org/dev/peps/pep-0008/

We *do* make a few exceptions and provide additional guidance which is documented in our `developer docs`_.

.. _developer docs: https://docs.develmaycare.com/en/developer/

Dependencies
============

.. include:: _includes/project-dependencies.rst

Tests
=====

.. include:: _includes/project-tests.rst

Releasing
=========

commonkit follows a loose form of `semantic versioning`_. The use of semantic versioning makes it clear when deprecation occurs and backward compatibility is removed. Documented incompatibilities may still exist where deprecation is not feasible (technically or financially).

.. _semantic versioning: https://semver.org/

Cadence
-------

New features may be planned for release every 3 months. Patch-level changes (to fix bugs or security issues) are always released as needed.

Long-Term Support
-----------------

Some releases may be designated as long-term support (LTS) releases. Such releases will have security and critical bug fixes applied for 6 months.

Deprecation Policy
------------------

Minor releases may deprecate features from a previous minor release. For example, if a feature is deprecated in release 1.1, it will continue to work in the 1.2 release, though warnings may be raised. However, the deprecated feature may be removed in release 1.3 and may not function as previously expected or will raise errors.

Major releases may *always* remove deprecated features.

Patch-level releases *never* remove deprecated features.

Legal
=====

.. code-block:: text

    Copyright (C) Pleasant Tents, LLC

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
       disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
       derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
